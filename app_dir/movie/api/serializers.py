from app_dir.movie.models import Movie
from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)


class FileUploadCheckSerializer(serializers.Serializer):
    status = serializers.DecimalField(max_digits=15, decimal_places=2)


class AverageUSABudgetMoviesSerializer(serializers.Serializer):
    budget_average = serializers.DecimalField(max_digits=15, decimal_places=2)


class TotalUSABudgetMoviesSerializer(serializers.Serializer):
    budget_total = serializers.DecimalField(max_digits=15, decimal_places=2)
