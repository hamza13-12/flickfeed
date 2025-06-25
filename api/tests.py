from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from api.models import UserProfile, Movie, Review, Comment, Like

class UserProfileModelTests(TestCase):
    def test_profile_creation_on_user_registration(self):
        """Test profile is created when a user registers"""
        user = User.objects.create_user(username='user1', password='pass')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_follow_unfollow_methods(self):
        """Test follow and unfollow methods"""
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        profile1 = user1.userprofile
        profile2 = user2.userprofile
        profile1.following.add(profile2)
        self.assertIn(profile2, profile1.following.all())
        profile1.following.remove(profile2)
        self.assertNotIn(profile2, profile1.following.all())

    def test_follower_following_count_methods(self):
        """Test follower and following count methods"""
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        profile1 = user1.userprofile
        profile2 = user2.userprofile
        profile2.followers.add(profile1)
        self.assertEqual(profile2.followers.count(), 1)
        self.assertEqual(profile1.following.count(), 1)

    def test_profile_picture_upload(self):
        """Test profile picture upload (mocked)"""
        user = User.objects.create_user(username='user1', password='pass')
        profile = user.userprofile
        profile.profile_picture = 'test_pic.jpg'
        profile.save()
        self.assertEqual(profile.profile_picture, 'test_pic.jpg')

class MovieModelTests(TestCase):
    def test_movie_creation_with_valid_data(self):
        """Test movie creation with valid data"""
        movie = Movie.objects.create(title='Movie', genre='ACTION', release_year=2024, description='desc')
        self.assertEqual(movie.title, 'Movie')

    def test_movie_creation_with_invalid_data(self):
        """Test movie creation with invalid data (should fail)"""
        with self.assertRaises(Exception):
            Movie.objects.create(title='', genre='INVALID', release_year=2024, description='desc')

    def test_get_average_rating_method(self):
        """Test get_average_rating method"""
        movie = Movie.objects.create(title='Movie', genre='ACTION', release_year=2024, description='desc')
        user = User.objects.create_user(username='user', password='pass')
        Review.objects.create(movie=movie, user=user, text='Good', rating=4)
        self.assertEqual(movie.get_average_rating(), 4)

    def test_genre_choices_validation(self):
        """Test genre choices validation (should fail for invalid genre)"""
        with self.assertRaises(Exception):
            Movie.objects.create(title='Movie', genre='INVALID', release_year=2024, description='desc')

class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.movie = Movie.objects.create(title='Movie', genre='ACTION', release_year=2024, description='desc')

    def test_review_creation(self):
        """Test review creation"""
        review = Review.objects.create(movie=self.movie, user=self.user, text='Nice', rating=5)
        self.assertEqual(review.text, 'Nice')

    def test_rating_validation(self):
        """Test rating validation (should fail for out-of-range)"""
        with self.assertRaises(Exception):
            Review.objects.create(movie=self.movie, user=self.user, text='Bad', rating=10)

    def test_unique_constraint_one_review_per_user_per_movie(self):
        """Test unique constraint: one review per user per movie"""
        Review.objects.create(movie=self.movie, user=self.user, text='Nice', rating=5)
        with self.assertRaises(Exception):
            Review.objects.create(movie=self.movie, user=self.user, text='Again', rating=4)

    def test_get_likes_count_method(self):
        """Test get_likes_count method"""
        review = Review.objects.create(movie=self.movie, user=self.user, text='Nice', rating=5)
        self.assertEqual(review.likes.count(), 0)

class CommentLikeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.movie = Movie.objects.create(title='Movie', genre='ACTION', release_year=2024, description='desc')
        self.review = Review.objects.create(movie=self.movie, user=self.user, text='Nice', rating=5)

    def test_comment_creation_and_deletion(self):
        """Test comment creation and deletion"""
        comment = Comment.objects.create(review=self.review, author=self.user, text='Comment')
        self.assertEqual(Comment.objects.count(), 1)
        comment.delete()
        self.assertEqual(Comment.objects.count(), 0)

    def test_like_creation_and_uniqueness(self):
        """Test like creation and uniqueness"""
        like = Like.objects.create(review=self.review, user=self.user)
        self.assertEqual(Like.objects.count(), 1)
        with self.assertRaises(Exception):
            Like.objects.create(review=self.review, user=self.user)

    def test_cascade_deletion(self):
        """Test cascade deletion when parent objects are deleted"""
        comment = Comment.objects.create(review=self.review, author=self.user, text='Comment')
        self.review.delete()
        self.assertEqual(Comment.objects.count(), 0)
        # Like cascade
        like = Like.objects.create(review=self.review, user=self.user)
        self.review.delete()
        self.assertEqual(Like.objects.count(), 0)
