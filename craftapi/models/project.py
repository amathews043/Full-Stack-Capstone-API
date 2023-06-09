from django.db import models 
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=75)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pattern_url = models.URLField(blank=True)
    hidden = models.BooleanField()
    description = models.CharField(max_length=5000)
