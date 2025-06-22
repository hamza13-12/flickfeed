from django.test import TestCase, RequestFactory
from api.models import Comment, Movie, Review
from api.permissions import IsCommentAuthorOrReadOnly
from django.contrib.auth.models import User

class IsCommentAuthorPermissionTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='auth', password='x')
        self.other = User.objects.create_user(username='other', password='x')
        self.movie = Movie.objects.create(
            title="PermTest", genre="DRAMA", release_year=2022, description="Testing perms"
        )
        self.review = Review.objects.create(
            user=self.user, movie=self.movie, rating=4, text="Nice movie"
        )
        self.comment = Comment.objects.create(
            author=self.user,
            review=self.review,
            text="Hello"
        )

    def test_owner_can_edit(self):
        request = self.factory.put("/fake-path")
        request.user = self.user
        perm = IsCommentAuthorOrReadOnly()
        self.assertTrue(perm.has_object_permission(request, None, self.comment))

    def test_other_cannot_edit(self):
        request = self.factory.put("/fake-path")
        request.user = self.other
        perm = IsCommentAuthorOrReadOnly()
        self.assertFalse(perm.has_object_permission(request, None, self.comment))