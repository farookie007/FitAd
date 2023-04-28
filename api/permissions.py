from rest_framework import permissions


class IsHostPermission(permissions.BasePermission):
    """Permission fo the host of the `Room` object."""

    def has_object_permission(self, request, view, obj):
        """Only the `host` of the `Room` is permitted."""
        return bool(obj.host == request.session.session_key)
    
class IsMemberPermission(permissions.BasePermission):
    """Permission for the members of the `Room`."""
    def has_object_permission(self, request, view, obj):
        """Only the `host` and member of the `Room` has this permission."""
        is_host = (obj.host == request.session.session_key)
        is_member = (request.session.get("room_code") == obj.code)
        print(f"[PERMISSION]: \n\tis_host = {is_host}\n\tis_member = {is_member}")
        return bool(is_host or is_member)
