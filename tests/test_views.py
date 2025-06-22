from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Movie, Review, Like, UserProfile

class MovieViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='viewuser', password='x')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.movie = Movie.objects.create(
            title="MovieX", genre="DRAMA", release_year=2022, description="Drama movie"
        )

    def test_get_movies(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_review_endpoint(self):
        url = reverse('movie-reviews', kwargs={'pk': self.movie.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class LikeAndFollowTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='test123')
        self.user2 = User.objects.create_user(username='user2', password='test123')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)  # authzrize

        self.movie = Movie.objects.create(title='M', genre='ACTION', release_year=2023, description='Test')
        self.review = Review.objects.create(user=self.user2, movie=self.movie, text="Good", rating=4)

        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile



    def test_like_review(self):
        url = reverse('review-like', kwargs={'pk': self.review.pk})
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_double_like_not_allowed(self):
        url = reverse('review-like', kwargs={'pk': self.review.pk})
        self.client.post(url)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unlike_review(self):
        like_url = reverse('review-like', kwargs={'pk': self.review.pk})
        unlike_url = reverse('review-unlike', kwargs={'pk': self.review.pk})
        self.client.post(like_url)
        res = self.client.post(unlike_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_follow_user(self):
        url = reverse('userprofile-follow', kwargs={'pk': self.profile2.pk})
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_double_follow(self):
        url = reverse('userprofile-follow', kwargs={'pk': self.profile2.pk})
        self.client.post(url)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)  # still 200 but should avoid duplicate logic

    def test_unfollow_user(self):
        follow_url = reverse('userprofile-follow', kwargs={'pk': self.profile2.pk})
        unfollow_url = reverse('userprofile-unfollow', kwargs={'pk': self.profile2.pk})
        self.client.post(follow_url)
        res = self.client.post(unfollow_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)