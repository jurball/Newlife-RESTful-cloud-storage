from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from database.models import Files, FileAccess, CustomUser
from set_files_access.serializers import FileSerializer, FileAccessSerializer


class AccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, file_id):
        # Получаем файл по строковому ID
        file = get_object_or_404(Files, file_id=file_id)

        # Проверяем, является ли пользователь владельцем файла
        if file.user != request.user:
            return Response({"detail": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

        # Получаем email пользователя для добавления доступа
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)

        # Добавляем доступ
        FileAccess.objects.create(file=file, user=user)

        # Получаем список всех пользователей с доступом к файлу
        accesses = FileAccess.objects.filter(file=file)
        serializer = FileAccessSerializer(accesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, file_id):
        # Получаем файл по строковому ID
        file = get_object_or_404(Files, file_id=file_id)

        # Проверка, что пользователь является владельцем файла
        if file.user != request.user:
            return Response({"detail": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

        # Получаем email пользователя для удаления доступа
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)

        # Проверка, что не пытаемся удалить себя
        if user == request.user:
            return Response({"detail": "Cannot remove yourself."}, status=status.HTTP_403_FORBIDDEN)

        # Удаляем доступ
        access = FileAccess.objects.filter(file=file, user=user).first()
        if not access:
            return Response({"detail": "Access not found."}, status=status.HTTP_404_NOT_FOUND)

        access.delete()

        # Получаем обновленный список всех пользователей с доступом
        accesses = FileAccess.objects.filter(file=file)

        # Формируем список пользователей с доступом и их ролью
        response_data = []
        for access in accesses:
            fullname = f"{access.user.first_name} {access.user.last_name}".strip()
            if not fullname:
                fullname = access.user.email  # Если имени нет, возвращаем только email
            user_data = {
                "fullname": fullname,
                "email": access.user.email,
                "type": access.access_type
            }
            response_data.append(user_data)

        return Response(response_data, status=status.HTTP_200_OK) # НАДО ДОДЕЛАТЬ ВЫВОД РЕСПОНСА ПРИ КОРРЕКТНОМ УДАЛЕНИИ ФАЙЛА


class UserFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        files = Files.objects.filter(user=request.user)
        serializer = FileSerializer(files, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class SharedFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        files = Files.objects.filter(shared_with=request.user).exclude(user=request.user)
        serializer = FileSerializer(files, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)