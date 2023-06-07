from django.db import models
from datetime import datetime

class Note(models.Model):
    note = models.CharField(max_length=5000)
    date = models.DateField(default=datetime.now)
    project = models.ForeignKey("project", on_delete=models.CASCADE, related_name="project_notes")