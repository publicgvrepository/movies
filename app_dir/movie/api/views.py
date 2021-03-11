from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from django.db import IntegrityError, transaction
import csv, io
import json
from django.db.models import Avg, Sum
from decimal import Decimal

from .serializers import FileUploadSerializer, AverageUSABudgetMoviesSerializer, \
    TotalUSABudgetMoviesSerializer
from ..models import Movie


class FileUploadAPIView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        status_response = status.HTTP_201_CREATED
        content = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        decoded_file = file.read().decode('UTF-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        try:
            with transaction.atomic():
                for row in reader:
                    Movie.objects.create(
                        imdb_title_id = row['imdb_title_id'],
                        title = row['title'],
                        country = row['country'],
                        budget = row['budget'].split()[1] if row['budget'] else 0.0,
                        currency = row['budget'].split()[0] if row['budget'] else ""
                    )
        except Exception as e:
            content = json.dumps(e)
            status_response = status.HTTP_500_INTERNAL_SERVER_ERROR
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
        average['budget_average'] = round(average['budget_average'],2)
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