from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from craftapi.models import Comment, Post


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

class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'message', 'post', 'sender', 'date']

class createCommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Comment 
        fields = ['id', 'message', 'post']
