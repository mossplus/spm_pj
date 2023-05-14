from django.test import TestCase
from ..models import *
from ..services import StudentService


# reference:
#  https://docs.djangoproject.com/en/4.2/topics/testing/overview/
#  https://docs.python.org/3/library/unittest.html#module-unittes


class StudentTestCase(TestCase):

    def setUp(self):

        self.ids = [dct['id'] for dct in Student.objects.values('id')]
        self.stu_service = StudentService()

    def test_student_register_and_login(self):
        pass
        # self.stu_service.create_student_with_wx_id('wxid_b1e9l9ew37dv22')
        # self.assertEqual(self.stu_service.verify_student_with_wx_id('wxid_b1e9l9ew37dv22'), True)
        # self.stu_service.update_student_with_wx_id('wxid_b1e9l9ew37dv22',
        #                                            stu_id='10185101238', stu_name='xrliu', password='123')
        # self.assertEqual(self.stu_service.verify_student_with_stu_id(stu_id='10185101238'), True)
        # self.assertEqual(self.stu_service.verify_student_with_password(stu_id='10185101238',
        #                                                                password='123'), True)

    def tearDown(self):

        students = Student.objects.exclude(id__in=self.ids)
        students.delete()
