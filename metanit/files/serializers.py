from rest_framework import serializers
from database.models import Files


class FilesSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Files
        fields = ('success', 'message', 'name', 'url', 'file_id')

    def get_url(self, obj):
        return f"{self.context['request'].build_absolute_uri('/files/')}{obj.file_id}"