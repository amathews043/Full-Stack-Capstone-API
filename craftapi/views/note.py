from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from craftapi.models import Note


class NoteView(ViewSet):

    def list(self, request):
        notes = Note.objects.all()

        if "project_id" in request.query_params: 
            project_id = int(request.query_params['project_id'])
            notes = notes.filter(project=project_id)

        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

class NoteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Note
        fields = ('id', 'note', 'date', 'project')