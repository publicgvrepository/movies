import io
import os

import pandas as pd
from app_dir.movie.api.serializers import (AverageUSABudgetMoviesSerializer,
                                           FileUploadSerializer,
                                           TotalUSABudgetMoviesSerializer)
from app_dir.movie.models import Movie
from app_dir.movie.tasks import (error_handler, task_transaction_test,
                                 task_validating_csv)
from django.db.models import Avg, Sum
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView


class FileUploadAPIView(generics.CreateAPIView):
    """
    DB transaction in Celery task
    """
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        status_response = status.HTTP_201_CREATED
        content = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        decoded_file = file.read().decode('UTF-8')
        io_string = io.StringIO(decoded_file)
        df = pd.read_csv(io_string)
        file_name = f"/tmp/{file.name}"
        if os.path.exists(file_name):
            status_response = status.HTTP_400_BAD_REQUEST
            content = {'msj': "file already exists"}
        else:
            df.to_csv(file_name)
            task_chain = (task_validating_csv.s(file_name,) |
                          task_transaction_test.si(file_name)
                          ).on_error(error_handler.s()).apply_async()
            content = {'msj': "loadding movies"}
        return Response(content, status=status_response)


class AverageUSABudgetMoviesAPIView(APIView):

    def get(self, request, format=None):
        """
            Returns total budget from USA's movies
        """
        status_response = status.HTTP_200_OK
        content = {}
        average = Movie.objects \
            .filter(country__icontains='usa') \
            .aggregate(budget_average=Avg('budget'))
        average['budget_average'] = round(average['budget_average'], 2)
        serializer = AverageUSABudgetMoviesSerializer(data=average)
        if serializer.is_valid(raise_exception=True):
            content = serializer.data
        return Response(content, status=status_response)


class TotalUSABudgetMoviesAPIView(APIView):

    def get(self, request, format=None):
        """
            Returns total budget from USA's movies
        """
        status_response = status.HTTP_200_OK
        content = {}
        total = Movie.objects \
            .filter(country__icontains='usa') \
            .aggregate(budget_total=Sum('budget'))
        serializer = TotalUSABudgetMoviesSerializer(data=total)
        if serializer.is_valid(raise_exception=True):
            content = serializer.data
        return Response(content, status=status_response)
