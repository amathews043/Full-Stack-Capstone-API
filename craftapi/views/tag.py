from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from craftapi.models import Tag

class TagView(ViewSet):
    """Post View """
    
    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    

class TagSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag
        fields = ('id', 'tag')
    