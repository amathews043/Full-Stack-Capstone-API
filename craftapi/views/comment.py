from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from craftapi.models import Comment, Post, User
from django.db.models import Q
from rest_framework.decorators import action


class CommentView(ViewSet):
    def list(self, request):
        comments = Comment.objects.all()
        serializer = commentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk): 
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = commentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist as ex: 
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        sender = request.auth.user
        serializer = createCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=sender)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk): 
        comment = Comment.objects.get(pk=pk)
        user = User.objects.get(pk=comment.sender.id)
        if request.auth.user == user or request.auth.user.is_staff == True:
            comment.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "This is not a comment you made. You cannot delete other users' comments"}, status=status.HTTP_404_NOT_FOUND)
    
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
