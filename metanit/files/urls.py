from django.urls import path
from files.views import FileUploadView

urlpatterns = [
    path('files', FileUploadView.as_view(), name='upload-files'),
]