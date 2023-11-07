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
    return Response({
        "users": reverse("customuser-list", request=request, format=format),
        "rooms": reverse("room-list", request=request, format=format),
        "members": reverse("member-list", request=request, format=format),
    })


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

    def perform_create(self, serializer):
        room = Room.objects.filter(code=serializer.validated_data["room_code"])
        if room.exists():
            serializer.save(room=room.first())
        else:
            return Response(data={"detail": "Invalid room code"}, status=status.HTTP_400_BAD_REQUEST)
