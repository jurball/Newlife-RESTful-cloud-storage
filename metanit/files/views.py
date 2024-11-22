import string
import random
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from database.models import Files
from rest_framework.parsers import MultiPartParser
from files.serializers import FilesSerializer, FileEditSerializer
from files.utils import get_file_or_404, check_file_permission


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

            file_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            user_file = Files.objects.create(
                user=request.user,
                file=file,
                name=file.name,
                file_id=file_id,
            )

            serializer = FilesSerializer(user_file, context={'request': request})
            response_data.append({
                "success": True,
                "message": "success",
                **serializer.data
            })

        return Response(response_data, status=status.HTTP_200_OK)

class FileEmployView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, file_id, *args, **kwargs):
        file_or_error = get_file_or_404(file_id)
        if isinstance(file_or_error, Response):
            return file_or_error

        file = file_or_error
        permission_error = check_file_permission(file, request.user)
        if permission_error:
            return permission_error

        if os.path.exists(file.file.path):
            os.remove(file.file.path)

        file.delete()

        return Response({
            "success": True,
            "message": "File deleted",
        }, status=status.HTTP_200_OK)

    def patch(self, request, file_id, *args, **kwargs):
        file_or_error = get_file_or_404(file_id)
        if isinstance(file_or_error, Response):
            return file_or_error

        file = file_or_error
        permission_error = check_file_permission(file, request.user)
        if permission_error:
            return permission_error

        serializer = FileEditSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Renamed"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, file_id, *args, **kwargs):
        pass

