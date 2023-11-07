from rest_framework import serializers

from accounts.models import CustomUser
from rooms.models import Member, Room



class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    rooms = serializers.HyperlinkedRelatedField(view_name="room-detail", many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ("url", "id", "username", "email", "rooms")


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.HyperlinkedRelatedField(view_name="member-detail", many=True, read_only=True)
    class Meta:
        model = Room
        fields = ("url", "id", "host", "title", "code", "members")
        read_only_fields = ["host", "code"]

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.HyperlinkedRelatedField(view_name="room-detail", read_only=True)
    room_code = serializers.CharField(max_length=10, write_only=True)
    class Meta:
        model = Member
        fields = ("url", "id", "username", "room", "room_code")