from ..models import *


class StudentService:

    def verify_student_with_wx_id(self, wx_id):
        return Student.objects.filter(wx_id=wx_id).exists()

    def verify_student_with_stu_id(self, stu_id):
        return Student.objects.filter(stu_id=stu_id).exists()

    def verify_student_with_password(self, stu_id, password):
        student = Student.objects.get(stu_id=stu_id)
        return student.password == password

    def create_student_with_wx_id(self, wx_id):
        student = Student(wx_id=wx_id, email='', email_verify=True)
        student.save()
        return {}

    def update_student_with_wx_id(self, wx_id, stu_id, stu_name, password, email):
        student = Student.objects.get(wx_id=wx_id)
        student.stu_id = stu_id
        student.stu_name = stu_name
        student.email = email
        student.password = password
        student.save()
        return {}

    def select_student_with_stu_id(self, stu_id):
        student = Student.objects.get(stu_id=stu_id)
        return {'id': student.id, 'wx_id': student.wx_id, 'stu_id': student.stu_id, 'stu_name': student.stu_name}

    def delete_student_with_stu_id(self, stu_id):
        student = Student.objects.get(stu_id=stu_id)
        student.delete()
        return {}
