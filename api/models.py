from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class UserProfile(models.Model):
    """
    Extension of the User model with additional fields for social features.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def follow(self, user_profile):
        """
        Follow another user profile (if not already following).
        """
        if user_profile != self and not self.is_following(user_profile):
            self.following.add(user_profile)

    def unfollow(self, user_profile):
        """
        Unfollow another user profile (if currently following).
        """
        if self.is_following(user_profile):
            self.following.remove(user_profile)

    def is_following(self, user_profile):
        """
        Check if this profile is following another user profile.
        """
        return self.following.filter(id=user_profile.id).exists()

    def get_follower_count(self):
        """
        Return the number of followers (other users who follow this profile).
        """
        return self.followers.count()

    def get_following_count(self):
        """
        Return the number of users this profile is following.
        """
        return self.following.count()

class Movie(models.Model):
    """
    Movie model containing basic information about a movie.
    """
    GENRE_CHOICES = [
        ('ACTION', 'Action'),
        ('COMEDY', 'Comedy'),
        ('DRAMA', 'Drama'),
        ('FANTASY', 'Fantasy'),
        ('HORROR', 'Horror'),
        ('MYSTERY', 'Mystery'),
        ('ROMANCE', 'Romance'),
        ('THRILLER', 'Thriller'),
        ('SCI_FI', 'Science Fiction'),
    ]
    
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    release_year = models.IntegerField()
    description = models.TextField()
    poster_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.release_year})"
    
    # TODO: Add method to get average rating
    def get_average_rating(self):
        """
        Calculate and return the average rating from all reviews
        """
        result = self.reviews.aggregate(Avg('rating'))
        avg = result['rating__avg']
        return round(avg, 2) if avg is not None else 0

class Review(models.Model):
    """
    Review model for movie reviews with ratings.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['movie', 'user']  # One review per movie per user
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.movie.title}"
    
    # TODO: Add method to get likes count
    def get_likes_count(self):
        """
        Return the number of likes this review has received
        """
        return self.likes.count() # FK relation b/w likes and review, using ORM count method to get the data

class Comment(models.Model):
    """
    Comment model for user comments on reviews.
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.review}"

class Like(models.Model):
    """
    Like model for tracking likes on reviews.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'review']  # Prevent multiple likes by same user
    
    def __str__(self):
        return f"Like by {self.user.username} on {self.review}"
