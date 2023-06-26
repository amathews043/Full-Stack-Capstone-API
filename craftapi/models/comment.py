from django.db import models
from django.conf import settings
from datetime import datetime

class Comment(models.Model):
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
