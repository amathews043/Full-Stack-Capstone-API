from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from craftapi.models import Note, User, Project


class NoteView(ViewSet):

    def retrieve(self, request, pk):
        note = Note.objects.get(pk=pk)
        project = Project.objects.get(pk=note.project.id)
        user = User.objects.get(pk=request.auth.user.id)

        if user.id == project.user_id:
            serializer=NoteSerializer(note)
            return Response(serializer.data)
        else: 
            return Response({'message': "This is not your project. Notes can only be viewed by the project creator"}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request):
        notes = Note.objects.all()
        user = User.objects.get(pk=request.auth.user.id)

        if "project_id" in request.query_params: 
            project_id = int(request.query_params['project_id'])
            project = Project.objects.get(pk=project_id)

            if user.id == project.user_id:
                notes = notes.filter(project=project_id)
                serializer = NoteSerializer(notes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else: return Response({'message': "This is not your project. Notes can only be viewed by the project creator"}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        project = Project.objects.get(pk=request.data['project'])
        user = User.objects.get(pk=request.auth.user.id)
        if user.id == project.user_id:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: return Response({'message': "This is not you project. Notes can only be viewed by the project creator"}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk):

        note = Note.objects.get(pk=pk)
        project = Project.objects.get(pk=note.project.id)
        user = User.objects.get(pk=request.auth.user.id)

        if project.user_id == user.id:
            note.note=request.data['note']
            note.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        else: 
            return Response({'message': 'This is not your project. You cannot edit notes on other crafters projects'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        note=Note.objects.get(pk=pk)
        project = Project.objects.get(pk=note.project.id)
        user = User.objects.get(pk=request.auth.user.id)

        if project.user_id == user.id: 
            note.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'This is not your project. You cannot delete notes on other crafters projects'}, status=status.HTTP_401_UNAUTHORIZED)





class NoteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Note
        fields = ('id', 'note', 'date', 'project')