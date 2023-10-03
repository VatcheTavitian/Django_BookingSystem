from django.shortcuts import render, redirect
from django.views import View
from .models import ConferenceRoom, RoomReservation
from datetime import date


class AddRoomView(View):
    def get(self, request):
        return render(request, "add_room.html")

    def post(self, request):
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"

        if not name:
            return render(request, "add_room.html", context={"error": "Room name not entered"})
        if capacity <= 0:
            return render(request, "add_room.html", context={"error": "Capacity must be more than 1"})
        if ConferenceRoom.objects.filter(name=name).first():
            return render(request, "add_room.html", context={"error": "Room name already exists"})

        ConferenceRoom.objects.create(
            name=name, capacity=capacity, projector_availability=projector)
        return redirect("room-list")


class AllRooms(View):
    def get(self, request):
        curr_date = date.today()
        rooms = ConferenceRoom.objects.all()
        for room in rooms:
            reservation_dates = [
                reservation.date for reservation in room.roomreservation_set.all()]
            room.reserved = curr_date in reservation_dates
        return render(request, "rooms.html", context={"rooms": rooms, "curr_date": curr_date})


class DeleteRoomView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        room.delete()
        return redirect("room-list")


class ModifyRoomView(View):
    def get(self, request, room_id):
        rooms = ConferenceRoom.objects.get(id=room_id)
        return render(request, "modify_room.html", context={"room": rooms})

    def post(self, request, room_id):
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"

        if not name:
            return render(request, "add_room.html", context={"error": "Room name not entered"})
        if capacity <= 0:
            return render(request, "add_room.html", context={"error": "Capacity must be more than 1"})
        if ConferenceRoom.objects.filter(name=name).exclude(id=room_id).first():
            return render(request, "add_room.html", context={"error": "Room name already exists"})
        obj = ConferenceRoom.objects.get(id=room_id)
        obj.name = name
        obj.capacity = capacity
        obj.projector_availability = projector
        obj.save()
        return redirect("room-list")


class RoomReservationView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        room.reservations = [
            reservation for reservation in room.roomreservation_set.all()]
        return render(request, "reserve_room.html", context={"room": room})

    def post(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        date_ = request.POST.get("date")
        comment = request.POST.get("comment")
        current = date.today()

        if not date_:
            return render(request, "reserve_room.html", context={"room": room, "error": "You must enter a date"})
        if RoomReservation.objects.filter(date=date_, room_id_id=room_id):
            return render(request, "reserve_room.html", context={"room": room, "error": "Room is already booked that date!"})
        if date_ < str(current):
            return render(request, "reserve_room.html", context={"room": room, "error": "Date cannot be in past!"})
        RoomReservation.objects.create(
            room_id=room, date=date_, comment=comment)
        return redirect("room-list")


class RoomView(View):
    def get(self, request, room_id):
        roominfo = RoomReservation.objects.filter(
            room_id_id=room_id).order_by('date')
        roomonly = ConferenceRoom.objects.get(id=room_id)
        if roominfo:
            return render(request, "room_view.html", context={"roominfo": roominfo})
        else:
            return render(request, "room_view.html", context={"roomonly": roomonly})


class SearchView(View):
    def get(self, request):
        return render(request, "search.html")

    def post(self, request):
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector") == "on"
        rooms = ConferenceRoom.objects.all()
        if projector:
            rooms = rooms.filter(projector_availability=projector)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms = rooms.filter(name__contains=name)

        for room in rooms:
            reservation_dates = [
                reservation.date for reservation in room.roomreservation_set.all()]
            room.reserved = date.today() in reservation_dates

        return render(request, "search.html", context={"rooms": rooms})
