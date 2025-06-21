# Testing Guide for FlickFeed

Before submitting your PR, ensure you've written and run the following tests:

## 1. Model Tests (`tests/test_models.py`)

### UserProfile Tests
```python
- Test profile creation on user registration
- Test follow/unfollow methods
- Test follower/following count methods
- Test profile picture upload
```

### Movie Tests
```python
- Test movie creation with valid data
- Test movie creation with invalid data (validation)
- Test get_average_rating method
- Test genre choices validation
```

### Review Tests
```python
- Test review creation
- Test rating validation (1-5)
- Test unique constraint (one review per user per movie)
- Test get_likes_count method
```

### Comment & Like Tests
```python
- Test comment creation and deletion
- Test like creation and uniqueness
- Test cascade deletion (when parent objects are deleted)
```

## 2. API Tests (`tests/test_views.py`)

### Authentication Tests
```python
- Test token obtain and refresh
- Test protected endpoint access with/without token
- Test permission classes
```

### UserProfile API Tests
```python
- Test profile retrieval (GET)
- Test profile update (PUT/PATCH)
- Test follow/unfollow endpoints
- Test feed endpoint
- Test following/followers list endpoints
```

### Movie API Tests
```python
- Test movie list and detail views
- Test movie creation (admin only)
- Test movie update and deletion
- Test movie filtering (by title, genre, year)
- Test movie reviews endpoint
```

### Review API Tests
```python
- Test review creation
- Test review update/deletion (owner only)
- Test like/unlike endpoints
- Test comments endpoint
- Test duplicate review prevention
```

## 3. Permission Tests (`tests/test_permissions.py`)
```python
- Test IsOwnerOrReadOnly permission
- Test IsReviewAuthorOrReadOnly permission
- Test IsCommentAuthorOrReadOnly permission
- Test CannotLikeTwice permission
```

## 4. Serializer Tests (`tests/test_serializers.py`)
```python
- Test nested serialization (UserProfile with User)
- Test read-only fields
- Test validation methods
- Test custom field methods (get_follower_count, etc.)
```

## 5. Integration Tests
```python
- Test complete user journey (register → follow → review → like)
- Test cascade effects (user deletion → profile deletion)
- Test feed generation with multiple users
```

## Example Test Case

Here's an example of how to write a test:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from api.models import UserProfile, Movie, Review

class ReviewTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create test movie
        self.movie = Movie.objects.create(
            title='Test Movie',
            genre='ACTION',
            release_year=2024,
            description='Test description'
        )
        # Get authentication token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_review(self):
        """Test creating a movie review"""
        data = {
            'movie': self.movie.id,
            'text': 'Great movie!',
            'rating': 5
        }
        response = self.client.post('/api/reviews/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().text, 'Great movie!')

    def test_duplicate_review(self):
        """Test user cannot review same movie twice"""
        # Create first review
        Review.objects.create(
            movie=self.movie,
            user=self.user,
            text='First review',
            rating=5
        )
        # Try to create second review
        data = {
            'movie': self.movie.id,
            'text': 'Second review',
            'rating': 4
        }
        response = self.client.post('/api/reviews/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Review.objects.count(), 1)
```

## Running Tests

Run all tests:
```bash
python manage.py test
```

Run specific test file:
```bash
python manage.py test tests.test_models
```

Run specific test case:
```bash
python manage.py test tests.test_models.ReviewTests
```

## Coverage Report

Generate a coverage report:
```bash
coverage run manage.py test
coverage report
coverage html  # For detailed HTML report
```

## PR Checklist

Before submitting your PR, ensure:

- [ ] All tests pass successfully
- [ ] Test coverage is at least 80%
- [ ] Both positive and negative test cases are included
- [ ] Edge cases are considered and tested
- [ ] Integration tests cover main user flows
- [ ] No existing tests were broken

## Best Practices

1. **Arrange-Act-Assert**: Structure your tests in three parts
   - Arrange: Set up test data
   - Act: Perform the action
   - Assert: Check the results

2. **Isolation**: Each test should be independent
   - Use setUp and tearDown methods
   - Don't rely on data from other tests

3. **Meaningful Names**: Test names should describe:
   - What is being tested
   - Under what circumstances
   - What is the expected result

4. **Test Edge Cases**: Include tests for:
   - Invalid inputs
   - Boundary conditions
   - Error scenarios

5. **Mock External Services**: Use mocking for:
   - External API calls
   - File operations
   - Email sending

Remember: Tests are as important as the feature itself. They ensure your code works as intended and prevent future regressions. 