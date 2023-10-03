"""BookingAppProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from booking_app.views import AddRoomView, AllRooms, DeleteRoomView, ModifyRoomView, \
	RoomReservationView, RoomView, SearchView

urlpatterns = [
    path('admin/', admin.site.urls),
	path('room/new/', AddRoomView.as_view(), name="add-room"),
	path('room-list/', AllRooms.as_view(), name="room-list"),
	path('room/delete/<int:room_id>/', DeleteRoomView.as_view(), name="delete_room"),
	path('room/modify/<int:room_id>/', ModifyRoomView.as_view(), name="modify_room"),
	path('room/reserve/<int:room_id>/', RoomReservationView.as_view(), name="reserve_room"),
	path('room/room_view/<int:room_id>/', RoomView.as_view(), name="room_view"),
	path('room/search/', SearchView.as_view(), name="search"),
]
