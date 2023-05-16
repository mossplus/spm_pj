from django.views import View
from ..APIResponse import APIResponse
from ..services import StudentService
import json


class RegisterView(View):

    stu_service = StudentService()

    def get(self, request) -> APIResponse:
        return APIResponse(status='405', data={}, error='Method Not Allowed')

    def post(self, request) -> APIResponse:
        try:
            data = json.loads(request.body)
            wx_id = data.get("wx_id")
            if not self.stu_service.verify_student_with_wx_id(wx_id=wx_id):
                self.stu_service.create_student_with_wx_id(wx_id=wx_id)
                self.stu_service.update_student_with_wx_id(wx_id=wx_id, stu_id=data.get("stu_id"), email=data.get("email"),
                                                           stu_name=data.get("stu_name"), password=data.get("password"))
                return APIResponse(status='201', data={}, error='')
            else:
                return APIResponse(status='401', data={}, error='User already exists')
        except Exception as e:
            return APIResponse(status='500', data={}, error=e)


class LoginView(View):

    stu_service = StudentService()

    def get(self, request) -> APIResponse:
        return APIResponse(status='405', data={}, error='Method Not Allowed')

    def post(self, request) -> APIResponse:
        try:
            data = json.loads(request.body)
            stu_id = data.get("stu_id")
            password = data.get("password")
            if self.stu_service.verify_student_with_stu_id(stu_id=stu_id):
                if not self.stu_service.verify_student_with_password(stu_id=stu_id, password=password):
                    return APIResponse(status='401', data={}, error='Invalid username or password')
                data = self.stu_service.select_student_with_stu_id(stu_id=stu_id)
                return APIResponse(status='200', data=data, error='')
            else:
                return APIResponse(status='401', data={}, error='No this user')
        except Exception as e:
            return APIResponse(status='500', data={}, error=e)


class LogoutView(View):
    pass
