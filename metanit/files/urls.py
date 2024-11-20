from django.urls import path
from files.views import FileUploadView, FileDeleteView

urlpatterns = [
    path('files', FileUploadView.as_view(), name='upload-files'),
    path('files/<str:file_id>/', FileDeleteView.as_view(), name='file-delete'),
]