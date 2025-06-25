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
        if hasattr(obj, 'followers'):
            return obj.followers.count()
        
    
    def get_following_count(self, obj):
        # TODO: Implement method to get following count
        if hasattr(obj, 'following'):
            return obj.following.count()
       
    
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
        if hasattr(obj, 'reviews') and obj.reviews.exists():
            total_rating = sum(review.rating for review in obj.reviews.all())
            return total_rating / obj.reviews.count()
        

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
        if hasattr(obj, 'likes'):
            return obj.likes.count()
        return 0
    
    def create(self, validated_data):
        # TODO: Implement proper creation logic with current user
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
    def validate(self, attrs):
        user = self.context['request'].user
        movie = attrs.get('movie')
        if Review.objects.filter(user=user, movie=movie).exists():
            raise serializers.ValidationError("You have already reviewed this movie.")
        return attrs
    
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
        user = self.context['request'].user
        validated_data['author'] = user 
        return super().create(validated_data)



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
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
    def validate(self, attrs):
        user = self.context['request'].user
        review = attrs.get('review')
        if Like.objects.filter(user=user, review=review).exists():
            raise serializers.ValidationError("You have already liked this review.")
        return attrs
    # TODO: Add validation to check if user has already liked this review 
