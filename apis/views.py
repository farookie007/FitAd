from django.contrib.sessions.models import Session
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .permissions import MemberPermisssion, RoomPermission
from .serializers import CustomUserSerializer, MemberSerializer, RoomSerializer
from accounts.models import CustomUser
from rooms.models import Member, Room


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("customuser-list", request=request, format=format),
            "rooms": reverse("room-list", request=request, format=format),
            "members": reverse("member-list", request=request, format=format),
        }
    )


class CustomUserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (RoomPermission,)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomList(generics.ListCreateAPIView):
    permission_classes = (RoomPermission,)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (MemberPermisssion,)
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def perform_update(self, serializer):
        return serializer.save(room=Room.objects.filter(code=serializer.validated_data["room_code"]).first())


class MemberList(generics.ListCreateAPIView):
    permission_classes = (MemberPermisssion,)
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def perform_create(self, serializer, room, session):
        return serializer.save(room=room, session=session)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # checking if the room exists
        room = Room.objects.filter(code=serializer.validated_data["room_code"]).first()
        if not room:
            return Response(
                data={"message": "Invalid Room code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # checking if the session exists
        if not request.session.session_key:
            request.session.create()
        session = Session.objects.get(pk=request.session.session_key)
        # check if the session already belong to a member
        # try assigning the room and session to the serializer
        try:
            self.perform_create(serializer, room, session)
        except IntegrityError:
            return Response(data={"message": f"You already belong in a room - {room.code}","room_url": reverse("room-detail", [room.pk], request=request, format=None)},
                            status=status.HTTP_403_FORBIDDEN)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
