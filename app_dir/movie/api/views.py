from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db import IntegrityError, transaction
import csv, io
import json
from decimal import Decimal

from .serializers import FileUploadSerializer
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
        # upload_products_csv.delay(decoded_file, request.user.pk)
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        try:
            with transaction.atomic():
                for row in reader:
                    Movie.objects.create(
                        imdb_title_id = row['imdb_title_id'],
                        title = row['title'],
                        country = row['country'],
                        budget = row['budget']
                    )
        except Exception as e:
            # Transaction failed - return a response notifying the client
            content = json.dumps(e)
            status_response = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(content, status=status_response)