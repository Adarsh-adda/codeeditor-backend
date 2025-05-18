from rest_framework import serializers
from .models import ExecutionResult

class CodeExecutionSerializer(serializers.Serializer):

    language = serializers.CharField(max_length=50)
    source_code = serializers.CharField()

    def validate_language(self, value):
        supported_languages = ['javascript', 'typescript', 'python', 'java', 'csharp', 'php']
        if value not in supported_languages:
            raise serializers.ValidationError(
                f"Language '{value}' is not supported. Supported languages: {', '.join(supported_languages)}")
        return value


class ExecutionResultSerializer(serializers.ModelSerializer):
    run = serializers.SerializerMethodField()

    class Meta:
        model = ExecutionResult
        fields = ['run']

    def get_run(self, obj):
        return {
            'output': obj.output,
            'stderr': obj.stderr,
            'execution_time': obj.execution_time
        }