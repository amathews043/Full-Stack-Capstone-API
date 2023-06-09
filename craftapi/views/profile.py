from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from craftapi.models import User

class ProfileView(ViewSet):
    def retrieve(self, request, pk):
        try:
            profile = User.objects.get(pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except User.DoesNotExist as ex: 
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk): 
        user = User.objects.get(pk=request.auth.user.id)

        if user.id == int(pk): 
            user.username = request.data['username']
            user.password = request.data['password']
            user.bio = request.data['bio']
            user.profile_pic = request.data['profile_pic']
            user.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        elif user.id == 1:
            update_user = User.objects.get(pk=pk)
            update_user.is_staff = request.data['is_staff']
            update_user.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        else: 
            return Response({'message': 'This is not your profile'}, status=status.HTTP_401_UNAUTHORIZED)
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ('id', 'username', 'first_name', 'is_staff', 'bio', 'profile_pic')
