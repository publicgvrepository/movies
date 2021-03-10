from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin', include('rest_framework.urls', namespace='rest')),
    path('api/movie/', include(('app_dir.movie.api.urls', 'movie_api'), \
        namespace='movie_api')),
]

