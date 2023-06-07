from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from models import Post

class PostView(ViewSet):
    """Post View """

    def retrieve(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostSerializer(serializers.ModelSerializer):
    class Meta: 
        model: Post
        fields = ('id', 'post', 'date', 'project', 'user')
