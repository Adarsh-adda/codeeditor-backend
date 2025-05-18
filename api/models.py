from django.db import models

# Create your models here.
class ExecutionResult(models.Model):
    language = models.CharField(max_length=50)
    source_code = models.TextField()
    output = models.TextField()
    stderr = models.TextField(blank=True, null=True)
    execution_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.language} execution on {self.created_at}"