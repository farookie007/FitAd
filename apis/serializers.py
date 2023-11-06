from rest_framework import serializers

from accounts.models import CustomUser
from rooms.models import Room



class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("url", "id", "username", "email", "room")


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ("url", "id", "host", "title", "code", "active")
        read_only_fields = ["host", "code", "active"]
