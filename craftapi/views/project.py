from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from craftapi.models import Project, User, Post

class ProjectView(ViewSet):

    def list(self, request): 
        user = User.objects.get(pk=request.auth.user.id)
        projects = Project.objects.all()

        if "my_projects" in request.query_params: 
            projects = projects.filter(user_id = user.id)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            projects = Project.objects.filter(hidden=False)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except Project.DoesNotExist as ex: 
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        user = User.objects.get(pk=request.auth.user.id)
        serializer = CreateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        user = User.objects.get(pk=request.auth.user.id)
        project = Project.objects.get(pk=pk)

        if user.id == project.user_id: 
            project.name = request.data['name']
            project.hidden = request.data['hidden']
            project.pattern_url = request.data['pattern_url']
            project.description = request.data['description']
            project.inspirations.set(request.data['inspirations'])

            project.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        else: 
            return Response({'message': 'This is not your project'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self,request, pk): 
        project = Project.objects.get(pk=pk)
        user = User.objects.get(pk=request.auth.user.id)

        if project.user_id == user.id or user.is_staff == True:
            project.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'This is not your project'}, status=status.HTTP_401_UNAUTHORIZED)


class ProjectSerializer(serializers.ModelSerializer):
    preview_image = serializers.ReadOnlyField()
    class Meta: 
        model = Project
        fields = ('id', 'name', 'pattern_url', 'hidden', 'description', 'user_id', 'project_posts', 'preview_image', 'inspirations', 'creator_name')
        depth = 1

class CreateProjectSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Project
        fields = ('id', 'name', 'pattern_url', 'hidden', 'description', 'inspirations')
        
