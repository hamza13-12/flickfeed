from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Movie, Review, Comment, Like

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        # TODO: Implement proper user serialization with password handling

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    """
    user = UserSerializer(read_only=True)
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_picture', 'follower_count', 'following_count']
    
    def get_follower_count(self, obj):
        # TODO: Implement method to get follower count
        return 0
    
    def get_following_count(self, obj):
        # TODO: Implement method to get following count
        return 0
    
    # TODO: Add additional methods for handling follow/unfollow actions

class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.
    """
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'release_year', 'description', 
                  'poster_url', 'created_at', 'average_rating']
    
    def get_average_rating(self, obj):
        # TODO: Implement method to calculate average rating
        return 0

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'text', 'rating', 'timestamp', 'likes_count']
        read_only_fields = ['user']
    
    def get_likes_count(self, obj):
        # TODO: Implement method to get likes count
        return 0
    
    def create(self, validated_data):
        # TODO: Implement proper creation logic with current user
        pass
    
    # TODO: Add validation to check if user has already reviewed this movie

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'review', 'author', 'text', 'timestamp']
        read_only_fields = ['author']
    
    def create(self, validated_data):
        # TODO: Implement proper creation logic with current user
        pass

class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'review', 'timestamp']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        # TODO: Implement proper creation logic with current user
        pass
    
    # TODO: Add validation to check if user has already liked this review 