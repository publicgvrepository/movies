from django.urls import path
from .views import FileUploadAPIView, AverageUSABudgetMoviesAPIView,\
    TotalUSABudgetMoviesAPIView

urlpatterns = [
    path('load', FileUploadAPIView.as_view(), name='movie-load'),
    path('total-usa', TotalUSABudgetMoviesAPIView.as_view(), name='usa-movie-total'),
    path('average-usa', AverageUSABudgetMoviesAPIView.as_view(), name='usa-movie-average')
]