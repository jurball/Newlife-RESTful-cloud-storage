from django.contrib import admin
from database.models import CustomUser, Files, FileAccess


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Основная информация", {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'file_id', 'name')

@admin.register(FileAccess)
class FileAccessAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'access_type')