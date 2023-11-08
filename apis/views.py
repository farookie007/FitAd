from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .permissions import IsHostOrReadOnly
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
    permission_classes = [IsAuthenticatedOrReadOnly, IsHostOrReadOnly]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberList(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # checking if the room exists
        room = Room.objects.filter(code=serializer.validated_data["room_code"])
        if not room.exists():
            return Response(
                data={"message": "Invalid Room code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # assigning the room to the serializer and saving rather than call `perform_create` method
        serializer.save(room=room.first())
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
