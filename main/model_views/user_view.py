from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from ..APIResponse import APIResponse
from ..models import *
import json
class RegisterView(View):
    def get(self, request):
        return APIResponse(status = '405', data = {}, error = 'Method Not Allowed')


    def post(self, request):
        pass

class LoginView(View):
    def get(self, request):
        return APIResponse(status = '405', data = {}, error = 'Method Not Allowed')

    def post(self, request):
        try:
            data = json.loads(request.body)
            stu_id = data.get("stu_id")
            password = data.get("password")
            if Student.objects.filter(stu_id=stu_id).exists():
                student = Student.objects.filter(stu_id=stu_id)[0]
                if student.password != password:
                    return APIResponse(status = '401', data = {}, error = 'Invalid username or password')
                data = {}
                data['id'] = student.id
                data['wx_id'] = student.id
                data['stu_id'] = student.stu_id
                data['stu_name'] = student.stu_name
                return APIResponse(status = '200', data = data , error = '')
            else:
                return APIResponse(status = '401', data = {}, error = 'No this user')
        except Exception as e:
            return APIResponse(status = '500', data = {} , error = e)

class LogoutView(View):
    pass
    # def get(self, request):
    #     logout(request)
    #     return redirect('login')
