from django.urls import path

from .views import CreateRoomView, JoinRoomView, DisplayRoomView, ListRoomView, CloseRoomView, LeaveRoomView, RoomRequestView, CreateRequestView, ListRequestView


app_name = "rooms"


urlpatterns = [
    path("display/", DisplayRoomView.as_view(), name="display_room"),
    path("<int:pk>/<str:code>/close/", CloseRoomView.as_view(), name="leave_room"),
    # path("close/", CloseRoomView.as_view(), name="leave_room"),
    path("leave/", LeaveRoomView.as_view(), name="leave_room"),
    path("create/", CreateRoomView.as_view(), name="create_room"),
    path("join/", JoinRoomView.as_view(), name="join_room"),
    path("list/", ListRoomView.as_view(), name="list_room"),
    path("request/create/", CreateRequestView.as_view(), name="create_req"),
    path("request/list/", ListRequestView.as_view(), name="list_req"),
    path("request_list/", RoomRequestView.as_view(), name="room_req_list"),
]
