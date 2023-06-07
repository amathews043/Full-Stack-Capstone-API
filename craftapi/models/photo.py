from django.db import models

class Photo(models.Model):
    image_url = models.URLField()
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="project_photos")