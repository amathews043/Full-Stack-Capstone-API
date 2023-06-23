from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
import os
import openai
from django.db.models import Q

from craftapi.models import Post, Project, User, Tag


class PostView(ViewSet):
    """Post View """

    def retrieve(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist as ex: 
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        posts = Post.objects.all().order_by('-id')

        if "project_id" in request.query_params: 
            project_id = int(request.query_params['project_id'])
            posts = posts.filter(project=project_id)

        if "user_id" in request.query_params:
            user_id = int(request.query_params['user_id'])
            posts = posts.filter(user=user_id)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
        user = User.objects.get(pk=request.auth.user.id)
        if post.user_id == user.id or user.is_staff == True:
            post.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response({'message': 'This is not your post'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = User.objects.get(pk=request.auth.user.id)

        if post.user_id == user.id:
            post.post = request.data['post']
            post.image = request.data['image']
            post.tags.set(request.data['tags'])

            project = Project.objects.get(pk=request.data['project'])
            post.project = project

            post.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        else: 
            return Response({'message': 'This is not your post'}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(methods=['get'], detail=False)
    def current_user_post_list(self, request): 
        profile = request.auth.user
        posts = Post.objects.filter(Q(user_id = profile))

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False)
    def post_list(self, request): 
        profile = request.auth.user
        posts = Post.objects.filter(~Q(user_id = profile))

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True)
    def other_user_post_list(self, request, pk): 
        profile = User.objects.get(pk=pk)
        posts = Post.objects.filter(Q(user_id = profile))

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(methods=['post'], detail=False)
    def autofillPost(self, request):
        """Post request for a user to sign up for an event"""
        project = Project.objects.get(pk=request.data['project'])
        notes = project.project_notes.all()

        note_list = []

        for note in notes:
            note_list.append(note.note)

        inspirations = project.inspirations.all()
        inspirations_list = []
        for inspiration in inspirations:
            inspirations_list.append(f"{inspiration.name} by {inspiration.creator_name}")

        posts = project.project_posts.all()
        posts_list = []
        for post in posts:
            posts_list.append(post.post)

        tags = Tag.objects.filter(id__in=request.data['tags'])
        tags_list = []

        for tag in tags: 
            tags_list.append(tag.tag)

        conversation = [{"role": "system", "content": " You never use quotation marks in your response. You create social media posts that sound like you are talking to a good friend. You will help people create posts about their craft projects. You will only use new thoughts and not include things from previous posts about the project. You will not response with quotation marks around your response. Your response will not include "" or '' ",
                        "role": "user", "content": f"Can you please help me make a social media post for this project? {project.name} {project.description} project notes = {note_list} post tags = {tags_list} this project was inspired by {inspirations_list}. other posts about this project {posts_list}"}]
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=conversation
            )
        response = response.choices[0].message.content

        return Response({'message': response}, status=status.HTTP_201_CREATED)


class TagSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag
        fields = ['id', 'tag']

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta: 
        model = Post
        fields = ('id', 'post', 'date', 'project', 'user', 'image', 'project_name', 'creator_name', 'tags')

class CreatePostSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Post
        fields = ('id', 'post', 'image', 'tags')
