from rest_framework import permissions

    
class IsHostPermission(permissions.BasePermission):
    """Permission for the host of the Room object."""
    def has_object_permission(self, request, view, obj):
        """Only the host has this permission"""
        return obj.host == request.session.session_key


class IsNotHostPermission(permissions.BasePermission):
    """Permission not for the host of the Room object."""
    def has_object_permission(self, request, view, obj):
        """Only the host has this permission"""
        return obj.host != request.session.session_key


class IsMemberPermission(permissions.BasePermission):
    """Permission for the Members in the Room (including the 
    host)."""
    def has_object_permission(self, request, view, obj):
        """Only the host has this permission"""
        return (obj.host == request.session.session_key) or (request.session.get("room_code") == obj.code)
