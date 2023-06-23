from django.db import models
from .tag import Tag
from .project import Project
from django.conf import settings
from datetime import datetime

class Post(models.Model):
    post = models.CharField(max_length=5000)
    tags = models.ManyToManyField(Tag, related_name="post_tags")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_posts")
    image = models.URLField(blank=True)

    @property
    def project_name(self):
        return f'{self.project.name}'
    
    @property 
    def creator_name(self):
        return f'{self.user.username}'
