from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from craftapi.models import Comment, Post
from django.db.models import Q
from rest_framework.decorators import action


class CommentView(ViewSet):
    def list(self, request):
        comments = Comment.objects.all()
        serializer = commentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk): 
        comment = Comment.objects.get(pk=pk)
        serializer = commentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        sender = request.auth.user
        serializer = createCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=sender)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['get'], detail=True)
    def post_comments_list(self, request, pk): 
        post = Post.objects.get(pk = pk)
        comments = Comment.objects.filter(Q(post_id = post.id))

        serializer = commentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'message', 'post', 'sender', 'date', 'sender_name']

class createCommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Comment 
        fields = ['id', 'message', 'post']
