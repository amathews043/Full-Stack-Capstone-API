from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from craftapi.models import Post, Project, User

class PostView(ViewSet):
    """Post View """

    def retrieve(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex: 
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        project = Project.objects.get(pk=request.data['project'])
        user = User.objects.get(pk=request.auth.user.id)
        if user.id == project.user_id:
            serializer = CreatePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response({'message': 'This is not your project'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    

class PostSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Post
        fields = ('id', 'post', 'date', 'project', 'user', 'image', 'project_name', 'creator_name')

class CreatePostSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Post
        fields = ('id', 'post', 'image')
