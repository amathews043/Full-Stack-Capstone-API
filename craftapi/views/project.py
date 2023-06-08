from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from craftapi.models import Project, User

class ProjectView(ViewSet):

    def list(self, request): 
        user = User.objects.get(pk=request.auth.user.id)
        projects = Project.objects.all()

        if "my_projects" in request.query_params: 
            projects = projects.filter(user_id = user.id)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)




class ProjectSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Project
        fields = ('id', 'name', 'patternURL', 'hidden', 'description', 'user_id')
