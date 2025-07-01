from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, Movie, Review, Comment, Like
from .serializers import (
    UserSerializer, UserProfileSerializer, MovieSerializer,
    ReviewSerializer, CommentSerializer, LikeSerializer
)
from .permissions import IsOwnerOrReadOnly, IsReviewAuthorOrReadOnly, IsCommentAuthorOrReadOnly, CannotLikeTwice

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # TODO: Add endpoint to view user profile
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """
        Get the user profile for a specific user.
        """
        user = self.get_object()
        profile = UserProfile.objects.filter(user=user).first()
        if profile:
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing user profiles.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    # TODO: Implement custom action for following/unfollowing users
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """
        Follow a user profile.
        """
        # TODO: Implement follow logic
        user_to_follow = self.get_object()
        user_profile = request.user.userprofile
        user_profile.following.add(user_to_follow)
        user_to_follow.followers.add(user_profile)
        user_profile.save()
        user_to_follow.save()
        return Response({"detail": "Followed successfully"}, status=status.HTTP_200_OK)
        # return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """
        Unfollow a user profile.
        """
        # TODO: Implement unfollow logic
        user_to_unfollow = self.get_object()
        user_profile = request.user.userprofile     
        user_profile.following.remove(user_to_unfollow)
        user_to_unfollow.followers.remove(user_profile)
        user_profile.save()
        user_to_unfollow.save()
        return Response({"detail": "Unfollowed successfully"}, status=status.HTTP_200_OK)
        # return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    # TODO: Implement custom action to get user's feed (reviews from followed users)
    @action(detail=False, methods=['get'])
    def feed(self, request):
        """
        Get the authenticated user's feed of reviews from followed users.
        """
        # TODO: Implement feed logic
        user_profile = request.user.userprofile
        followed_users = user_profile.following.all()
        reviews = []
        for user in followed_users:
            user_reviews = Review.objects.filter(user=user)
            reviews.extend(user_reviews)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing movie instances.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # TODO: Add endpoint to view movie reviews
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """
        Get all reviews for a specific movie.
        """
        # TODO: Implement reviews retrieval logic
        movie = self.get_object()
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED
        
    
    # TODO: Add search and filtering functionality
    def get_queryset(self):
        """
        Optionally filter movies based on query parameters.
        """
        # TODO: Implement filtering by title, genre, release year
        title = self.request.query_params.get('title', None)
        genre = self.request.query_params.get('genre', None)
        release_year = self.request.query_params.get('release_year', None)
        if title:
            self.queryset = self.queryset.filter(title__icontains=title)
        if genre:
            self.queryset = self.queryset.filter(genre=genre)
        if release_year:
            self.queryset = self.queryset.filter(release_year=release_year)
            return self.queryset
        # If no filters are applied, return all movies
        return self.queryset
   
class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing review instances.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsReviewAuthorOrReadOnly]
    
    # TODO: Override perform_create to set the user
    def perform_create(self, serializer):
        """
        Set the user when creating a review.
        """

        # TODO: Implement user assignment
        
        pass
    
    # TODO: Add endpoint to like/unlike a review
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        Like a review.
        """
        # TODO: Implement like logic
        return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """
        Unlike a review.
        """
        # TODO: Implement unlike logic
        return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    # TODO: Add endpoint to list comments on a review
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get all comments for a specific review.
        """
        # TODO: Implement comments retrieval logic
        return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing comment instances.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]
    
    # TODO: Override perform_create to set the author
    def perform_create(self, serializer):
        """
        Set the author when creating a comment.
        """
        
        # TODO: Implement author assignment

        pass

class LikeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing like instances.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, CannotLikeTwice]
    
    # TODO: Override perform_create to set the user
    def perform_create(self, serializer):
        """
        Set the user when creating a like.
        """
        # TODO: Implement user assignment
        pass
    
    # TODO: Add validation to prevent multiple likes
