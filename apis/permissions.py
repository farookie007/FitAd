from rest_framework.permissions import BasePermission



class IsHostOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.host == request.user