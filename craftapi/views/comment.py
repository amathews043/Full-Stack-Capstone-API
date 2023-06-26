from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from craftapi.models import Comment 

class CommentView(ViewSet): 
    def list(self, request): 
        Comment.objects.all()



class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment 
        fields = ['id', 'message', 'post', 'sender', 'date']