
from .model_views import *

from .services import rsv_services


def login(request):
    login_view = LoginView()
    if request.method == 'GET':
        return login_view.get(request=request)
    if request.method == 'POST':
        return login_view.post(request=request)


def register(request):
    register_view = RegisterView()
    if request.method == 'GET':
        return register_view.get(request=request)
    if request.method == 'POST':
        return register_view.post(request=request)


def stu_index(request, stu_id):
    index_view = IndexView()
    if request.method == 'GET':
        return index_view.get(request=request, stu_id=stu_id)
    if request.method == 'POST':
        return index_view.post(request=request, stu_id=stu_id)


def stu_room(request, stu_id, building_id):
    room_view = RoomView()
    if request.method == 'GET':
        return room_view.get(request=request, stu_id=stu_id, building_id=building_id)
    if request.method == 'POST':
        return room_view.post(request=request, stu_id=stu_id, building_id=building_id)


def stu_seat(request, stu_id, room_id):
    seat_view = SeatView()
    if request.method == 'GET':
        return seat_view.get(request=request, stu_id=stu_id, room_id=room_id)
    if request.method == 'POST':
        return seat_view.post(request=request, stu_id=stu_id, room_id=room_id)


def stu_record(request, stu_id):
    record_view = RecordView()
    if request.method == 'GET':
        return record_view.get(request=request, stu_id=stu_id)
    if request.method == 'POST':
        return record_view.post(request=request, stu_id=stu_id)


def test(request):
    if request.method == 'GET':
        r = rsv_services.ReservationService()
        r.send_reminder_as_email(1)
        return APIResponse(200, {}, {})


def qrcode(request, seat_id):
    qrview = QRcodeView()
    if request.method == 'GET':
        return qrview.get(request=request, seat_id=seat_id)


def signin(request):
    signin_view = SigninView()
    if request.method == 'GET':
        return signin_view.get(request=request)
    if request.method == 'POST':
        return signin_view.post(request=request)


# def mng_index(request, manager_id):
#     pass
#
#
# def mng_building(request, manager_id, building_id):
#     pass
#
#
# def mng_room(request, manager_id, room_id):
#     pass
