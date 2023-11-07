from django.urls import path

from .views import (
    api_root,
    CustomUserDetail,
    CustomUserList,
    MemberDetail,
    MemberList,
    RoomDetail,
    RoomList,
)


urlpatterns = [
    path("", api_root, name="api-root"),
    path("users/", CustomUserList.as_view(), name="customuser-list"),
    path("users/<int:pk>/", CustomUserDetail.as_view(), name="customuser-detail"),
    path("rooms/", RoomList.as_view(), name="room-list"),
    path("rooms/<int:pk>/", RoomDetail.as_view(), name="room-detail"),
    path("members/", MemberList.as_view(), name="member-list"),
    path("members/<int:pk>/", MemberDetail.as_view(), name="member-detail"),
]