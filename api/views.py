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
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def profile(self, request, pk=None):
        """
        Get the user profile for a specific user.
        """
        user = self.get_object()
        try:
            profile = user.profile  # thanks to related_name='profile'
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing user profiles.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        """
        Follow a user profile.
        """
        target = self.get_object()
        current = request.user.profile
        if current == target:
            return Response({"detail": "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        current.follow(target)
        return Response({"detail": f"You are now following {target.user.username}."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        """
        Unfollow a user profile.
        """
        target = self.get_object()
        current = request.user.profile
        current.unfollow(target)
        return Response({"detail": f"You unfollowed {target.user.username}."}, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        """
        Get the authenticated user's feed of reviews from followed users.
        """
        current = request.user.profile
        followed_users = current.following.all()
        reviews = Review.objects.filter(user__profile__in=followed_users).order_by('-timestamp')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing movie instances.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def reviews(self, request, pk=None):
        """
        Get all reviews for a specific movie.
        """
        movie = self.get_object()
        reviews = movie.reviews.all()  # uses related_name='reviews'
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        """
        Optionally filter movies based on query parameters.
        """
        queryset = Movie.objects.all()
        title = self.request.query_params.get('title')
        genre = self.request.query_params.get('genre')
        year = self.request.query_params.get('year')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre:
            queryset = queryset.filter(genre__iexact=genre)
        if year:
            queryset = queryset.filter(release_year=year)

        return queryset

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing review instances.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsReviewAuthorOrReadOnly]
    

    def perform_create(self, serializer):
        """
        Set the user when creating a review.
        """
        serializer.save(user=self.request.user)
    
 
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        Like a review.
        """
        review = self.get_object()
        user = request.user
        if Like.objects.filter(user=user, review=review).exists():
            return Response({"detail": "You already liked this review."}, status=status.HTTP_400_BAD_REQUEST)
        Like.objects.create(user=user, review=review)
        return Response({"detail": "Review liked."}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        Unlike a review.
        """
        review = self.get_object()
        user = request.user
        like = Like.objects.filter(user=user, review=review).first()
        if not like:
            return Response({"detail": "You haven't liked this review."}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({"detail": "Review unliked."}, status=status.HTTP_204_NO_CONTENT)
    
  
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def comments(self, request, pk=None):
        """
        Get all comments for a specific review.
        """
        review = self.get_object()
        comments = review.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing comment instances.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]
    

    def perform_create(self, serializer):
        """
        Set the author when creating a comment.
        """
        serializer.save(author=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing like instances.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, CannotLikeTwice]
    
  
    def perform_create(self, serializer):
        """
        Set the user when creating a like.
        """
        serializer.save(user=self.request.user)
    
    # TODO: Add validation to prevent multiple likes ######## <- ALR ADDED IN SERIALIZER.PY
