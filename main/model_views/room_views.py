from django.views import View
from ..APIResponse import APIResponse
from ..services import StudentService, BuildingService, RoomService, SeatService, ReservationService
import json


class IndexView(View):

    stu_service = StudentService()
    building_service = BuildingService()

    def get(self, request, stu_id) -> APIResponse:
        try:
            latitude = request.GET['latitude']
            longitude = request.GET['longitude']
            if self.stu_service.verify_student_with_stu_id(stu_id=stu_id):
                student = self.stu_service.select_student_with_stu_id(stu_id=stu_id)
                buildings = self.building_service.select_buildings_and_sort(latitude=latitude, longitude=longitude)
                return APIResponse(status='200', data={'student': student, 'buildings': buildings}, error='')
            else:
                return APIResponse(status='401', data={}, error='No this user')
        except Exception as e:
            return APIResponse(status='500', data={}, error=e)

    def post(self, request, stu_id) -> APIResponse:
        return APIResponse(status='405', data={}, error='Method Not Allowed')


class RoomView(View):

    stu_service = StudentService()
    building_service = BuildingService()
    room_service = RoomService()

    def get(self, request, stu_id, building_id) -> APIResponse:
        try:
            latitude = request.GET['latitude']
            longitude = request.GET['longitude']
            if self.stu_service.verify_student_with_stu_id(stu_id=stu_id):
                student = self.stu_service.select_student_with_stu_id(stu_id=stu_id)
                if self.building_service.verify_building_with_building_id(building_id=building_id):
                    building = self.building_service.select_building_with_building_id(building_id=building_id,
                                                                                      latitude=latitude, longitude=longitude)
                    rooms = self.room_service.select_rooms_and_sort(building_id=building_id)
                    return APIResponse(status='200', data={'student': student, 'building': building, 'rooms': rooms}, error='')
                else:
                    return APIResponse(status='404', data={}, error='No this building')
            else:
                return APIResponse(status='401', data={}, error='No this user')
        except Exception as e:
            return APIResponse(status='500', data={}, error=e)

    def post(self, request, stu_id, building_id) -> APIResponse:
        return APIResponse(status='405', data={}, error='Method Not Allowed')


class SeatView(View):

    stu_service = StudentService()
    room_service = RoomService()
    seat_service = SeatService()
    rsv_service = ReservationService()

    def get(self, request, stu_id, room_id) -> APIResponse:
        try:
            start_time = request.GET['start_time']
            end_time = request.GET['end_time']
            if self.stu_service.verify_student_with_stu_id(stu_id=stu_id):
                student = self.stu_service.select_student_with_stu_id(stu_id=stu_id)
                if self.room_service.verify_room_with_room_id(room_id=room_id):
                    room = self.room_service.select_room_with_room_id(room_id=room_id)
                    seats = self.seat_service.select_seats(room_id=room_id, start_time=start_time, end_time=end_time)
                    return APIResponse(status='200', data={'student': student, 'room': room, 'seats': seats}, error='')
                else:
                    return APIResponse(status='404', data={}, error='No this classroom')
            else:
                return APIResponse(status='401', data={}, error='No this user')
        except Exception as e:
            return APIResponse(status='500', data={}, error=e)

    def post(self, request, stu_id, room_id) -> APIResponse:
        try:
            data = json.loads(request.body)
            seat_id = data.get("seat_id")
            start_rsv_time = data.get("start_rsv_time")     # '%Y-%m-%d %H:%M'
            end_rsv_time = data.get("end_rsv_time")         # '%Y-%m-%d %H:%M'
            if self.stu_service.verify_student_with_stu_id(stu_id=stu_id):
                student = self.stu_service.select_student_with_stu_id(stu_id=stu_id)
                if self.room_service.verify_room_with_room_id(room_id=room_id):
                    if self.seat_service.verify_seat_with_seat_id(seat_id=seat_id):
                        self.rsv_service.create_reservation(student=student, start_rsv_time=start_rsv_time,
                                                            end_rsv_time=end_rsv_time, seat_id=seat_id)
                        return APIResponse(status='201', data={}, error='')
                    else:
                        return APIResponse(status='404', data={}, error='No this seat')
                else:
                    return APIResponse(status='404', data={}, error='No this classroom')
            else:
                return APIResponse(status='401', data={}, error='No this user')
        except Exception as e:
            return APIResponse(status='500', data={}, error=e)
