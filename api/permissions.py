from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the object.
        # TODO: Implement owner check logic
        # Write permissions are only allowed to the owner of the object.
        # The intern should implement the owner check based on the object type.
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user
      
        

class IsReviewAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow access to review authors only.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of the review
        # The intern should implement the author check
        # TODO: Implement author check logic
        # Only the author of a review should be able to edit or delete it
        # The intern should implement the author check

        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
    
        return False
    
            
     
        

class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow access to comment authors only.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # TODO: Implement author check logic
        # Only the author of a comment should be able to edit or delete it
        # The intern should implement the author check
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user 
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        return False

class CannotLikeTwice(permissions.BasePermission):
    """
    Custom permission to prevent users from liking a review more than once.
    """
    
    def has_permission(self, request, view):
        # TODO: Implement the check to prevent multiple likes
        # The intern should implement validation logic to check if the user
        # has already liked the specified review
        if hasattr(view, 'kwargs') and 'review_id' in view.kwargs:
            review_id = view.kwargs['review_id']
            user = request.user
            if user.is_authenticated:
                if hasattr(user, 'likes'):
                    return not user.likes.filter(review_id=review_id).exists()
        return True 