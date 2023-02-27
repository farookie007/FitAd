from rest_framework import serializers
# Local imports
from .models import Room, Requests


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "code",
            "host",
            "created_time",
        )
class DisplayRoomSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Room
        fields = ()

class JoinRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "code",
        )

class RequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = (
            "id",
            "song_title",
            "artiste",
            "sender_ID",
            "room",
            "timestamp",
        )

class CreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = (
            "song_title",
            "artiste",
        )
