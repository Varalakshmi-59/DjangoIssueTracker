from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Project
from users.models import User
from .serializers import ProjectSerializer, UserSerializer

# API to view all projects
class ProjectListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all projects.
        """
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API to view details of a specific project
class ProjectDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """
        Retrieve details of a specific project by ID.
        """
        try:
            project = Project.objects.get(id=project_id)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

# API to view all users (Admin Only)
class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all users (Admin only).
        """
        if not request.user.is_staff:  # Check if the user is an admin
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API to view details of a specific user
class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        """
        Retrieve details of a specific user by ID.
        """
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)