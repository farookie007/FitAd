from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
# Local imports
from rooms.models import Room, Request
from .serializers import RoomSerializer, CreateRoomSerializer, JoinRoomSerializer,\
    CreateRequestSerializer, RequestSerializer, DisplayRoomSerializer
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
                return Response(
                    RoomSerializer(room).data,
                    status=status.HTTP_200_OK,
                )
            else:
                room = Room(host=host)
                room.save()
                self.request.session["room_code"] = room.code
                return Response(
                    RoomSerializer(room).data,
                    status=status.HTTP_201_CREATED,
                )
        return Response(
            {"Bad Request": "Invalid data..."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    

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
                return Response(
                    {"message": "Room Joined successfully"},
                    status=status.HTTP_200_OK,
                )
            # if the room does not exists
            return Response(
                {"Bad Request": "Invalid Room Code. Try Again."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"Bad Request": "Invalid Parameters. No `code` key found."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DisplayRoomView(APIView):
    model = Room
    queryset = Room.objects.all()
    # permission_classes = (IsMemberPermission,)
    serializer_class = DisplayRoomSerializer

    @permission_classes([IsMemberPermission])
    def get(self, request, format=None):
        room_code = self.request.session.get("room_code")
        if room_code is not None:
            room = Room.objects.filter(code=room_code).first()
            if room:
                data = self.serializer_class(room).data
                data["is_host"] = (room.host == self.request.session.session_key)
                return Response(
                    data,
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"Not Found": "This room does not exist or has been closed by the host"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"Bad Request": "You don't belong in any room."},
            status=status.HTTP_400_BAD_REQUEST,
        )



class CloseRoomView(APIView):
    model = Room
    # permission_classes = (IsHostPermission,)
    queryset = Room.objects.all()


    @permission_classes([IsHostPermission])
    def delete(self, request, format=None):
        # confirms that the user is in `Room`
        room_code = self.request.session.get("room_code")
        # if the user does not belong in a `Room`, erase his `Room`
        if room_code is None:
            return Response(
                {"Bad Request": "You don't belong in any room."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.request.session["room_code"] = None
        # checks if the `Room` exists
        room = Room.objects.filter(code=room_code)
        # delete the `Room`
        if room:
            room.delete()
            return Response(
                {"message": "Closed Room successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"Bad Request": "You don't belong in any room."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LeaveRoomView(APIView):
    model = Room
    queryset = Room.objects.all()
    # Fix: check permission for this view
    # to only allow members and not host
    # permission_classes = (IsNotHostPermission,)

    @permission_classes([IsNotHostPermission])
    def post(self, request, format=None):
        # confirms that the user is in room
        if self.request.session.get("room_code"):
            self.request.session["room_code"] = None
            return Response(
                {"message": "Left Room successfully."},
                status=status.HTTP_200_OK,
            )
        # if the user does not belong in the room
        return Response(
            {"Bad Request": "Not a member in this Room."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ListRoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRequestView(APIView):
    serializer_class = CreateRequestSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            room_code = self.request.session.get("room_code")
            room = Room.objects.filter(code=room_code).first()
            if room:
                song_title = serializer.data.get("song_title")
                artiste = serializer.data.get("artiste")
                req = Request(
                    song_title=song_title,
                    artiste=artiste,
                    sender_ID=self.request.session.session_key,
                    room=room
                )
                req.save()
                return Response(
                    {"message": "Request created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"Bad Request": "You don't belong in a Room OR the Room is closed by the host."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"Bad Request": "Invalid data..."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ListRequestView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class RoomRequestView(APIView):
    serializer_class = RequestSerializer

    def get(self, request, format=None):
        room_code = self.request.session.get("room_code")
        if room_code is not None:
            room = Room.objects.filter(code=room_code).first()
            if room:
                return Response(
                    [self.serializer_class(req).data for req in room.user_requests.all()],
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"Bad Request": "You don't belong in a Room OR the Room is closed by the host."},
            status=status.HTTP_400_BAD_REQUEST,
        )