from django.urls import path
from .views import FileUploadAPIView

urlpatterns = [
    path('load', FileUploadAPIView.as_view(), name='movie-load'),
]