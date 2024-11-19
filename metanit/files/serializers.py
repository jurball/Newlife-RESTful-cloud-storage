from rest_framework import serializers
from database.models import Files


class FilesSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Files
        fields = ('file', 'user', 'name', 'file_id', 'url')  # Добавляем поле 'url'

    def get_url(self, obj):
        # Формируем абсолютный URL для файла
        return self.context['request'].build_absolute_uri(f'/files/{obj.file_id}/')