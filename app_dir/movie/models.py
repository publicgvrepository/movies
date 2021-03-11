from django.db import models

class Movie(models.Model):
    """
        Movie model data
        imdb_title_id: tt0000574
        title: The Story of the Kelly Gang
        original_title: The Story of the Kelly Gang
        year: 1906
        date_published: 1906-12-26
        genre: ,"Biography, Crime, Drama"
        duration: 70
        country: Australia
        language: None
        director: Charles Tait
        writer: ,Charles Tait
        production_company: J. and N. Tait
        actors: "Elizabeth Tait, John Tait, Norman Campbell, Bella Cola, Will Coyne, Sam Crewes, Jack Ennis, John Forde, Vera Linden, Mr. Marshall, Mr. McKenzie, Frank Mills, Ollie Wilson"
        description: True story of notorious Australian outlaw Ned Kelly (1855-80).
        avg_vote: 6.1
        votes: 589
        budget: $ 2250 ---> currency = $, budget = 2250
        usa_gross_income:
        worlwide_gross_income:
        metascore:
        reviews_from_users: 7.0
        reviews_from_critics: 7.0
    """
    imdb_title_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    currency = models.CharField(max_length=4)
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} - {self.country}'
