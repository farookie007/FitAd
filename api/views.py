from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
# Local imports
from .serializers import CreateRoomSerializer, RoomSerializer, JoinRoomSerializer, CreateRequestSerializer, RequestSerializer, DisplayRoomSerializer
from .permissions import IsHostPermission, IsMemberPermission
from rooms.models import Room, Request


HTTP_200_OK = status.HTTP_200_OK
HTTP_201_CREATED = status.HTTP_201_CREATED
HTTP_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND


class CreateRoomView(generics.CreateAPIView):
    """View to create a `Room` object."""

    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # if the session does not exist, create one
        STATUS = HTTP_201_CREATED
        SESSION_KEY = self.request.session.session_key
        if not self.request.session.exists(SESSION_KEY):
            self.request.session.create()
        
        SESSION_KEY = self.request.session.session_key
        host = SESSION_KEY
        serializer = self.serializer_class(data=request.data)
        # if the supplied info are valid
        if serializer.is_valid():
            queryset = Room.objects.filter(host=host)
            # if the host already has a room created
            if queryset.exists():
                room = queryset.first()
                self.request.session["room_code"] = room.code
                STATUS = HTTP_200_OK

            # if the host never created a room
            else:
                room = Room(host=host)
                room.save()
                self.request.session["room_code"] = room.code

            return Response(
                RoomSerializer(room).data,
                status=STATUS,
            )
        return Response(
            {"Bad Request": "Invalid data..."},
            status = HTTP_400_BAD_REQUEST,
        )


class JoinRoomView(APIView):
    """View to add a member to the `Room`."""
    serializer_class = JoinRoomSerializer

    def post(self, request, format=None):
        STATUS = HTTP_200_OK
        SESSION_KEY = self.request.session.session_key
        # if the session does not exist, create one
        if not self.request.session.exists(SESSION_KEY):
            self.request.session.create()
        # getting the `room_code` from the request
        code = request.data.get("code")
        # if the code is successfully obtained
        if code is not None:
            room = Room.objects.filter(code=code).first()
            # if the room exists
            if room:
                self.request.session["room_code"] = code
                return Response(
                    {"message": "Room Joined successfully"},
                    status = STATUS,
                )
            # if the room does not exist
            return Response(
                {"Bad Request": "Invalid Room code. Try Again."},
                status = HTTP_404_NOT_FOUND,
            )
        # if not `code` data is supplied
        return Response(
            {"Bad Request": "Invalid Parameters. No `code` found."},
            status = HTTP_400_BAD_REQUEST,
        )


class DisplayRoomView(generics.RetrieveAPIView):
    """View to display the room which the user belongs to."""
    model = Room
    serializer_class = DisplayRoomSerializer

    def get(self, request, format=None):
        STATUS = HTTP_200_OK

        # retrieving the `room_code`
        room_code =  self.request.session.get("room_code")
        if room_code is not None:
            room = self.model.objects.filter(code=room_code).first()
            # if the `room` exists
            if room:
                # serialize the `room` and add the `is_host` field
                data = self.serializer_class(room).data
                data["is_host"] = bool(room.host == self.request.session.session_key)
                return Response(
                    data,
                    status = STATUS,
                )
            # if the `room` does not exist
            return Response(
                {"Not Found": "The requested room does not exist or has been closed by the host"},
                status = HTTP_404_NOT_FOUND,
            )
        # if the request does not contain a `room_code`
        return Response(
            {"Bad Request": "You don't belong in any room"},
            status = HTTP_400_BAD_REQUEST,
        )
    

class CloseRoomView(generics.DestroyAPIView):
    model = Room

    def delete(self, request, format=None):
        # confirms that the user belongs in a room
        room_code = self.request.session.get("room_code")
        # if the user does not belong in a `Room`
        if room_code is None:
            return Response(
                {"Bad Request": "You don't belong in any room"},
                status = HTTP_400_BAD_REQUEST,
            )
        room = self.model.objects.filter(code=room_code).first()
        # checks if the room exists
        if room:
            # checks if the user is the host of the `Room`
            if room.host == self.request.session.session_key:
                self.request.session["room_code"] = None
                room.delete()
                return Response(
                    {"message": "Room closed successfully."},
                    status = HTTP_201_CREATED,
                )
            return Response(
                {"Bad Request": "Invalid credentials. Only host can close a Room"},
                status = HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"Bad Request": "Room does not exist."},
            status = HTTP_400_BAD_REQUEST,
        )

class LeaveRoomView(APIView):
    model = Room

    def get(self, request, format=None):
        room_code = self.request.session.get("room_code")
        # confirms that the user is a member of the room
        if room_code is not None:
            room = self.model.objects.filter(code=room_code).first()
            # if the room exists
            if room:
                # checks if the user is not the host
                if room.host != self.request.session.session_key:
                    self.request.session["room_code"] = None
                    return Response(
                        {"message": "Left Room successfully."},
                        status = HTTP_200_OK,
                    )
                return Response(
                    {"Bad Request": "Invalid credentials. Only members can leave a Room."},
                    status = HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"Bad Request": "Room does not exist or has been closed by the host."},
                status = HTTP_404_NOT_FOUND,
            )
            
        return Response(
            {"Bad Request": "You don't belong in any room"},
            status = HTTP_400_BAD_REQUEST,
        )


class ListRoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRequestView(generics.CreateAPIView):
    serializer_class = CreateRequestSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # gets the `Room` object
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
