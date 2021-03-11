from rest_framework import serializers
from ..models import Movie
from django.db.models import Avg, Sum


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)


class AverageUSABudgetMoviesSerializer(serializers.Serializer):
    budget_average = serializers.DecimalField(max_digits=15, decimal_places=2)

class TotalUSABudgetMoviesSerializer(serializers.Serializer):
    budget_total = serializers.DecimalField(max_digits=15, decimal_places=2)

