from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .permissions import IsHostOrReadOnly
from .serializers import CustomUserSerializer, RoomSerializer
from accounts.models import CustomUser
from rooms.models import Room



@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "users": reverse("customuser-list", request=request, format=format),
        "rooms": reverse("room-list", request=request, format=format),
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
