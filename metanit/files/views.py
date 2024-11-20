from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import ValidationError
from database.models import Files
from rest_framework.parsers import MultiPartParser
from files.serializers import FilesSerializer
import os

allowed_types = ["application/pdf",
                 "application/msword",
                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                 "application/zip",
                 "image/jpeg",
                 "image/png"
]

class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files[]')

        if not files:
            return Response({
                "success": False,
                "message": "No files provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        response_data = []

        for file in files:
            if file.size > 2 * 1024 * 1024:
                response_data.append({
                    "success": False,
                    "message": f"File {file.name} exceeds 2 MB size limit",
                })
                continue


            if file.content_type not in allowed_types:
                response_data.append({
                    "success": False,
                    "message": f"File {file.name} has an unsupported file type",
                })
                continue

            user_file = Files.objects.create(
                user=request.user,
                file=file,
                name=file.name
            )

            serializer = FilesSerializer(user_file, context={'request': request})
            response_data.append({
                "success": True,
                "message": "success",
                **serializer.data
            })

        return Response(response_data, status=status.HTTP_200_OK)

class FileDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, file_id, *args, **kwargs):
        try:
            file = Files.objects.get(file_id=file_id)
        except Files.DoesNotExist:
            return Response({
                "success": False,
                "message": "File does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        if file.user != request.user:
            return Response({
                "success": False,
                "message": "You do not have permission to delete this file",
            }, status=status.HTTP_403_FORBIDDEN)

        if os.path.exists(file.file.path):
            os.remove(file.file.path)

        file.delete()

        return Response({
            "success": True,
            "message": "File deleted",
        }, status=status.HTTP_200_OK)
