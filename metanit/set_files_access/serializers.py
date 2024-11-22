from rest_framework import serializers
from database.models import Files, FileAccess


class FileAccessSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    type = serializers.CharField(source='access_type')

    class Meta:
        model = FileAccess
        fields = ['full_name', 'email', 'type']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class FileSerializer(serializers.ModelSerializer):
    accesses = FileAccessSerializer(source='fileaccess_set', many=True, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Files
        fields = ['file_id', 'name', 'url', 'accesses']

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f"/files/{obj.id}")