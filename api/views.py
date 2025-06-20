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
        return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """
        Unfollow a user profile.
        """
        # TODO: Implement unfollow logic
        return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    # TODO: Implement custom action to get user's feed (reviews from followed users)
    @action(detail=False, methods=['get'])
    def feed(self, request):
        """
        Get the authenticated user's feed of reviews from followed users.
        """
        # TODO: Implement feed logic
        return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)

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
        return Response({"detail": "Not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    # TODO: Add search and filtering functionality
    def get_queryset(self):
        """
        Optionally filter movies based on query parameters.
        """
        # TODO: Implement filtering by title, genre, release year
        return Movie.objects.all()

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
