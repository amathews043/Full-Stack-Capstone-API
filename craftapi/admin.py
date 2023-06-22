from django.contrib import admin
from .models import Note, Post, Project, Tag, User

# Register your models here.
admin.site.register(Note)
admin.site.register(Post)
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(User)