from django.db import models
from .project import Project
from django.db.models import F, Q, CheckConstraint

class Inspiration(models.Model): 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    inspiration_project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_inspirations")

    class Meta:
        constraints = [
            CheckConstraint(name='not_same', check=~Q(project=F('inspiration_project')))
        ]