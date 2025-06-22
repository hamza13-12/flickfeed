# tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from api.models import UserProfile, Movie, Review, Comment, Like

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='test')
        self.user2 = User.objects.create_user(username='user2', password='test')
        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile

    def test_str_representation(self):
        self.assertEqual(str(self.profile1), "user1's profile")

    def test_follow_unfollow(self):
        self.profile1.follow(self.profile2)
        self.assertIn(self.profile2, self.profile1.following.all())
        self.assertIn(self.profile1, self.profile2.followers.all())

        self.profile1.unfollow(self.profile2)
        self.assertNotIn(self.profile2, self.profile1.following.all())

    def test_follower_following_count(self):
        self.profile1.follow(self.profile2)
        self.assertEqual(self.profile2.get_follower_count(), 1)
        self.assertEqual(self.profile1.get_following_count(), 1)

    def test_cannot_follow_self(self):
        self.profile1.follow(self.profile1)
        self.assertNotIn(self.profile1, self.profile1.following.all())

class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            genre="ACTION",
            release_year=2022,
            description="A movie."
        )

    def test_str_representation(self):
        self.assertEqual(str(self.movie), "Test Movie (2022)")

    def test_average_rating(self):
        user1 = User.objects.create_user(username='u1', password='x')
        user2 = User.objects.create_user(username='u2', password='x')
        Review.objects.create(user=user1, movie=self.movie, rating=4, text='Good')
        Review.objects.create(user=user2, movie=self.movie, rating=2, text='Okay')
        self.assertEqual(self.movie.get_average_rating(), 3.0)

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='revuser', password='x')
        self.movie = Movie.objects.create(title="M1", genre="ACTION", release_year=2022, description="Desc")
        self.review = Review.objects.create(user=self.user, movie=self.movie, rating=5, text="Great")

    def test_str(self):
        self.assertEqual(str(self.review), f"Review by {self.user.username} for {self.movie.title}")

    def test_likes_count(self):
        user2 = User.objects.create_user(username='u2', password='x')
        Like.objects.create(user=user2, review=self.review)
        self.assertEqual(self.review.get_likes_count(), 1)

    def test_duplicate_review_not_allowed(self):
        with self.assertRaises(IntegrityError):
            Review.objects.create(user=self.user, movie=self.movie, rating=4, text="Again")

    def test_invalid_rating(self):
        with self.assertRaises(ValidationError):
            bad_review = Review(user=self.user, movie=self.movie, rating=6, text="Too high")
            bad_review.full_clean()

class CommentModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username='cuser', password='x')
        movie = Movie.objects.create(title="M2", genre="COMEDY", release_year=2021, description="Desc")
        review = Review.objects.create(user=user, movie=movie, rating=4, text="Nice")
        comment = Comment.objects.create(author=user, review=review, text="Thanks")
        self.assertEqual(str(comment), f"Comment by {user.username} on {review}")

    def test_blank_comment(self):
        user = User.objects.create_user(username='cx', password='x')
        movie = Movie.objects.create(title="M3", genre="COMEDY", release_year=2021, description="Desc")
        review = Review.objects.create(user=user, movie=movie, rating=3, text="OK")
        with self.assertRaises(ValidationError):
            comment = Comment(author=user, review=review, text="")
            comment.full_clean()

class LikeModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username='luser', password='x')
        movie = Movie.objects.create(title="M3", genre="DRAMA", release_year=2020, description="Desc")
        review = Review.objects.create(user=user, movie=movie, rating=5, text="Perfect")
        like = Like.objects.create(user=user, review=review)
        self.assertEqual(str(like), f"Like by {user.username} on {review}")

    def test_duplicate_like_not_allowed(self):
        user = User.objects.create_user(username='dup', password='x')
        movie = Movie.objects.create(title="D", genre="HORROR", release_year=2019, description="Spooky")
        review = Review.objects.create(user=user, movie=movie, rating=4, text="Scary")
        Like.objects.create(user=user, review=review)
        with self.assertRaises(IntegrityError):
            Like.objects.create(user=user, review=review)
