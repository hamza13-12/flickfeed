# FlickFeed - Social Movie API

FlickFeed is a social platform for movie enthusiasts to share reviews, follow other users, and engage with content through comments and likes.

## 🎬 Project Overview

This is a skeleton project built with Django and Django Rest Framework. It provides the basic structure for a social movie review platform, with placeholders for implementation details that you, as an intern, will complete.

## 📋 Requirements

- Python 3.8+
- Django 4.2+
- Django Rest Framework (DRF)
- Other dependencies as specified in `requirements.txt`

## 🚀 Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flickfeed
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following content:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Load sample data:
   ```
   python manage.py loaddata api/fixtures/sample_data.json
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```
   python manage.py runserver
   ```

The API will be available at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/).

## 📂 Project Structure

- `api/models.py`: Contains all model definitions
- `api/serializers.py`: DRF serializers for each model
- `api/views.py`: ViewSets for handling API endpoints
- `api/permissions.py`: Custom permission classes
- `api/urls.py`: URL routing configuration

## 🎯 Models

1. **UserProfile**
   - Extension of the User model
   - Contains bio, profile picture, followers/following

2. **Movie**
   - Basic movie information including title, genre, year, description
   - Poster URL for displaying movie images

3. **Review**
   - Text review of a movie with a 1-5 rating
   - Created by a user for a specific movie

4. **Comment**
   - Text comment on a review
   - Created by a user

5. **Like**
   - Represents a user liking a review
   - Unique per user-review combination

## 📝 TODO Items for Interns

Here are the tasks for you to complete:

### UserProfile Model
- [ ] Implement `follow` and `unfollow` methods
- [ ] Add proper follower and following count methods

### Movie Model
- [ ] Implement `get_average_rating` method that calculates the average from review ratings

### Review Model
- [ ] Implement `get_likes_count` method

### Serializers
- [ ] Complete serializer create/update methods to handle nested relationships
- [ ] Add validation to prevent duplicate reviews/likes

### Views
- [ ] Implement feed logic in `UserProfileViewSet.feed` to show reviews from followed users
- [ ] Complete the follow/unfollow endpoints in `UserProfileViewSet`
- [ ] Add filtering to the `MovieViewSet.get_queryset` method (by title, genre, year)
- [ ] Implement like/unlike endpoints in `ReviewViewSet`
- [ ] Add proper user assignment in `perform_create` methods

### Permissions
- [ ] Implement proper permission checking in each permission class

## 🔍 Sample API Requests

Here are some example Postman requests you can try:

### Authentication
```
POST /api/token/
Body: {"username": "your_username", "password": "your_password"}
```

### Movies
```
GET /api/movies/
GET /api/movies/1/
POST /api/movies/ (with appropriate data)
```

### Reviews
```
GET /api/reviews/
POST /api/reviews/ (with movie_id, text, and rating)
POST /api/reviews/1/like/ (to like a review)
```

### User Profiles
```
GET /api/profiles/
POST /api/profiles/1/follow/ (to follow a user)
GET /api/profiles/feed/ (to see reviews from followed users)
```

## 📈 Extension Ideas

Once you've completed the basic tasks, consider these extensions:

1. Add search functionality with Django filters
2. Implement user recommendations based on viewing/rating history
3. Add JWT token blacklisting for better security
4. Implement a rate-limiting system for API requests
5. Create a proper API documentation using Swagger or ReDoc

## 📄 License

This project is provided for educational purposes only.

---

Happy coding! 🎬🍿 