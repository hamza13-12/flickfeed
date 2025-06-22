from django.test import TestCase
from api.models import Movie, Review
from api.serializers import MovieSerializer, ReviewSerializer
from django.contrib.auth.models import User

class MovieSerializerTest(TestCase):
    def test_movie_serializer_output(self):
        movie = Movie.objects.create(title="Title", genre="ACTION", release_year=2020, description="Desc")
        data = MovieSerializer(movie).data
        self.assertEqual(data['title'], "Title")
        self.assertIn('average_rating', data)

class ReviewSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="rev", password="123")
        self.movie = Movie.objects.create(title="Movie", genre="ACTION", release_year=2021, description="Desc")

    def test_review_duplicate_validation(self):
        Review.objects.create(user=self.user, movie=self.movie, rating=4, text="Good")
        data = {'movie': self.movie.id, 'text': "Another", 'rating': 5}
        context = {'request': type('obj', (object,), {'user': self.user})}
        serializer = ReviewSerializer(data=data, context=context)
        self.assertFalse(serializer.is_valid())