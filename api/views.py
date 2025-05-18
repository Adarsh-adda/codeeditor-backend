import subprocess
import time
import os
import tempfile
import shutil
from pathlib import Path

from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ExecutionResult
from .serializers import CodeExecutionSerializer, ExecutionResultSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class CodeExecutionView(APIView):
    """
    API view for executing code in various programming languages.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CodeExecutionSerializer(data=request.data)
        if serializer.is_valid():
            language = serializer.validated_data['language']
            source_code = serializer.validated_data['source_code']

            try:
                execution_result = self.execute_code(language, source_code)
                result_obj = ExecutionResult.objects.create(
                    language=language,
                    source_code=source_code,
                    output=execution_result['output'],
                    stderr=execution_result.get('stderr', ''),
                    execution_time=execution_result['execution_time']
                )
                response_serializer = ExecutionResultSerializer(result_obj)
                return Response(response_serializer.data)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                )

        return Response(serializer.errors)

    def execute_code(self, language, source_code):
        # Create a temporary directory to store and execute code
        temp_dir = tempfile.mkdtemp()

        try:
            # Define execution configurations for different languages
            config = self.get_language_config(language)
            file_path = Path(temp_dir) / config['file_name']

            # Write the source code to the file
            with open(file_path, 'w') as f:
                f.write(source_code)

            start_time = time.time()

            # Execute the code
            process = subprocess.run(
                config['command'],
                cwd=temp_dir,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10  # Timeout after 10 seconds
            )

            execution_time = time.time() - start_time

            return {
                'output': process.stdout,
                'stderr': process.stderr,
                'execution_time': execution_time
            }

        finally:
            # Clean up the temporary directory
            shutil.rmtree(temp_dir)

    def get_language_config(self, language):
        """Return the configuration for the specified language."""
        configs = {
            'javascript': {
                'file_name': 'main.js',
                'command': 'node main.js',
                'version': '18.15.0'
            },
            'typescript': {
                'file_name': 'main.ts',
                'command': 'tsc main.ts && node main.js',
                'version': '5.0.3'
            },
            'python': {
                'file_name': 'main.py',
                'command': 'python main.py',
                'version': '3.10.0'
            },
            'java': {
                'file_name': 'Main.java',
                'command': 'javac Main.java && java Main',
                'version': '15.0.2'
            },
            'csharp': {
                'file_name': 'main.cs',
                'command': 'dotnet script main.cs',
                'version': '6.12.0'
            },
            'php': {
                'file_name': 'main.php',
                'command': 'php main.php',
                'version': '8.2.3'
            }
        }

        if language not in configs:
            raise ValueError(f"Language '{language}' is not supported")

        return configs[language]