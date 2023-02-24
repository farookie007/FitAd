from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """Only authenticated users can see list view."""
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Read permissions are allowed to any request so we'll always allow GET, HEAD, or OPTIONS requests."""
        return (request.method in permissions.SAFE_METHODS) or (obj.author == request.user)
    
class IsHostPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Only the host has this permission"""
        return obj.host == request.session.session_key


class IsNotHostPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Only the host has this permission"""
        return obj.host != request.session.session_key

class IsMemberPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Only the host has this permission"""
        return (obj.host == request.session.session_key) or (request.session.get("room_code") == obj.code)