from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import ValidationError
from database.models import Files
from files.serializers import FilesSerializer
import os

allowed_types = ["application/pdf"
                 "application/msword",
                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                 "application/zip",
                 "image/jpeg",
                 "image/png"
]

class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        files = request.FILES.get('file')
        print(files)

        if not files:
            return Response({
                "success": False,
                "message": "No files provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        response_data = []

        for file in files:
            if file.size > 2 * 1024 * 1024:
                response_data.append({
                    "success": True,
                    "message": f"File {file.name} exceeds 2 MB size limit",
                })
                continue


            if file.content_type not in allowed_types:
                response_data.append({
                    "success": False,
                    "message": f"File {file.name} has an unsupported file type",
                })
                continue
            file_name = file.name
            file_extension = os.path.splitext(file.name)[1]

            counter = 1
            while Files.objects.filter(user=request.user, name=file_name).exists():
                file_name = f"{os.path.splitext(file.name)[0]} ({counter}){file_extension}"
                counter += 1

            user_file = Files.objects.create(
                user=request.user,
                file=file,
                name=file_name,
            )

            serializer = FilesSerializer(user_file, context={'request': request})
            response_data.append({
                "success": True,
                "message": "success",
                **serializer.data
            })

        return Response(response_data, status=status.HTTP_200_OK)