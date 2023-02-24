from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
# Local imports
from .serializers import RoomSerializer, CreateRoomSerializer, JoinRoomSerializer
from .models import Room
from .permissions import IsHostPermission, IsMemberPermission, IsNotHostPermission


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # if the session does not exist, create one
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        host = self.request.session.session_key
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset.first()
                self.request.session["room_code"] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=host)
                room.save()
                self.request.session["room_code"] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST)
    

class JoinRoomView(APIView):
    serializer_class = JoinRoomSerializer
    url_kwarg_lookup = "code"

    def post(self, request, format=None):
        # if the session does not exist, create one
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        # getting the room code from the request
        code = request.data.get(self.url_kwarg_lookup)
        if code is not None:
            room = Room.objects.filter(code=code).first()
            # if the room exists
            if room:
                self.request.session["room_code"] = code
                return Response({"message": "Room Joined successfully"}, status=status.HTTP_200_OK)
            # if the room does not exists
            return Response({"Bad Request": "Invalid Room Code. Try Again."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Bad Request": "Invalid Parameters. No `code` key found."}, status=status.HTTP_400_BAD_REQUEST)


class DisplayRoomView(generics.RetrieveAPIView):
    permission_classes = (IsMemberPermission,)
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class CloseRoomView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    # this ensures only the host can close a room
    permission_classes = (IsHostPermission,)


class LeaveRoomView(APIView):
    permission_classes = (IsNotHostPermission&IsMemberPermission,)
    def post(self, request, format=None):
        # confirms that the user is in room
        if self.request.session.get("room_code"):
            self.request.session["room_code"] = None
            return Response({"message": "Left Room successfully."}, status=status.HTTP_200_OK)
        # if the user does not belong in the room
        return Response({"Bad Request": "Not a member in this Room."}, status=status.HTTP_400_BAD_REQUEST)


class ListRoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer