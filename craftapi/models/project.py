from django.db import models 
from django.conf import settings
from django.db.models import Q

class Project(models.Model):
    name = models.CharField(max_length=75)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pattern_url = models.URLField(blank=True)
    hidden = models.BooleanField()
    description = models.CharField(max_length=5000)

    @property
    def preview_image(self):
        return self.project_posts.filter(~Q(image = None)).latest('id').image
