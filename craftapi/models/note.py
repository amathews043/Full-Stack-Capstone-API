from django.db import models

class Note(models.Model):
    note = models.CharField(max_length=5000)
    date = models.DateField(auto_now_add=True)
    project = models.ForeignKey("project", on_delete=models.CASCADE, related_name="project_notes")
