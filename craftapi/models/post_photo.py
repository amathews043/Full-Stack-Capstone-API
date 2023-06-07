from django.db import models

class PostPhoto(models.Model):
    image_url = models.URLField()
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_photos")