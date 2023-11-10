from django.contrib.sessions.models import Session
from rest_framework import permissions


class MemberPermisssion(permissions.BasePermission):
    def has_permission(self, request, view):
        # only users that does not belong in an active room - CREATE
        if request.method == "POST" and request.session.session_key:
            try:
                Session.objects.get(pk=request.session.session_key).member
                return False
            except:
                ...
        # Anyone - LIST
        return True

    def has_object_permission(self, request, view, obj):
        # only the `Member` - UPDATE
        SESSION_KEY = request.session.session_key
        if request.method in ["PUT", "PATCH"]:
            return obj.session_id == SESSION_KEY
        # only the `Room` host and the `Member` - RETRIEVE, DELETE
        return obj.room.host == request.user or obj.session_id == SESSION_KEY


class RoomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Anyone - LIST
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only authenticated User - CREATE
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only host or member - RETRIEVE
        if request.method in permissions.SAFE_METHODS:
            SESSION_KEY = request.session.session_key
            # checks if the member exists
            if member := obj.members.filter(session_id=SESSION_KEY).first():
                return request.user == obj.host or member.session_id == SESSION_KEY
        # Only the host - UPDATE, DELETE
        return request.user == obj.host
