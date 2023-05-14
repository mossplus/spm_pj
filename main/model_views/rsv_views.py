from django.views import View
from ..APIResponse import APIResponse
from ..services import StudentService, ReservationService
import json
from django.http import HttpResponse
from ..services import rsv_services


class RecordView(View):

    stu_service = StudentService()
    rsv_service = ReservationService()

    def get(self, request, stu_id) -> APIResponse:
        try:
            if self.stu_service.verify_student_with_stu_id(stu_id=stu_id):
                student = self.stu_service.select_student_with_stu_id(stu_id=stu_id)
                reservations = self.rsv_service.select_reservation_and_sort(student=student)
                return APIResponse(status='200', data={'student': student, 'reservations': reservations}, error='')
            else:
                return APIResponse(status='401', data={}, error='No this user')
        except Exception as e:
            return APIResponse(status='500', data={}, error=e)

    def post(self, request, stu_id) -> APIResponse:
        try:
            data = json.loads(request.body)
            rsv_id = data.get("rsv_id")
            if self.stu_service.verify_student_with_stu_id(stu_id=stu_id):
                if self.rsv_service.verify_reservation_with_rsv_id(rsv_id=rsv_id):
                    if self.rsv_service.verify_reservation_is_deletable(rsv_id=rsv_id):
                        self.rsv_service.delete_reservation_with_rsv_id(rsv_id=rsv_id)
                        return APIResponse(status='204', data={}, error='')
                    else:
                        return APIResponse(status='403', data={}, error='Time not permitted')
                else:
                    return APIResponse(status='404', data={}, error='No this reservation')
            else:
                return APIResponse(status='401', data={}, error='No this user')
        except Exception as e:
            return APIResponse(status='500', data={}, error=e)


class ReservationView(View):

    def get(self, request, stu_id) -> APIResponse:
        pass

    def post(self, request, stu_id) -> APIResponse:
        pass


class QRcodeView(View):

    rsv_service = rsv_services.ReservationService()

    def get(self, request, seat_id):
        signin_code = self.rsv_service.generate_signin_code(seatid=seat_id)
        byteIO = self.rsv_service.generate_qr_code(signin_code)
        return HttpResponse(byteIO.getvalue(), content_type='image/png')


class SigninView(View):

    rsv_service = rsv_services.ReservationService()

    def get(self, request) -> APIResponse:
        return APIResponse(status='405', data={}, error='Method Not Allowed')

    def post(self, request) -> APIResponse:
        try:
            data = json.loads(request.body)
            stu_id = data.get("stu_id")
            signin_code = data.get("signin_code")
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            data = self.rsv_service.signin_verify(stu_id=stu_id, signin_code=signin_code, latitude=latitude,
                                                  longitude=longitude)
            return APIResponse(status='200', data=data, error='')
        except Exception as e:
            return APIResponse(status='500', data={}, error=str(e))
