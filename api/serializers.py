from rest_framework import serializers
# Local imports
from rooms.models import Room, Request


class RoomSerializer(serializers.ModelSerializer):
    """Model serializer for the `Room` object."""
    class Meta:
        model = Room
        fields = (
            "id",
            "code",
            "host",
            "created_time",
        )


class DisplayRoomSerializer(serializers.ModelSerializer):
    """Model serializer for displaying the content of a room."""
    class Meta:
        model = Room
        fields = (
            "id",
            "code",
            "host",
            "created_time",
            "user_requests",
        )


class CreateRoomSerializer(serializers.ModelSerializer):
    """Model serializer for creating a `Room` object."""
    class Meta:
        model = Room
        fields = ()


class JoinRoomSerializer(serializers.ModelSerializer):
    """Model serializer for joining a `Room`."""
    class Meta:
        model = Room
        fields = (
            "code",
        )


class RequestSerializer(serializers.ModelSerializer):
    """Model serializer for the `Request` object."""
    class Meta:
        model = Request
        fields = (
            "id",
            "song_title",
            "artiste",
            "sender_ID",
            "room",
            "timestamp",
        )


class CreateRequestSerializer(serializers.ModelSerializer):
    """Model serializer for creating a `Request` object via API call."""
    class Meta:
        model = Request
        fields = (
            "song_title",
            "artiste",
        )