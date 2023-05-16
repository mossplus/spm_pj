from django.test import TestCase
from ..models import *
from ..services import *

# reference:
#  https://docs.djangoproject.com/en/4.2/topics/testing/overview/
#  https://docs.python.org/3/library/unittest.html#module-unittes

class SeatTestCase(TestCase):
    def setUp(self):
        Student.objects.create(id = 1, stu_id='1', stu_name='1', email='1', password='1', wx_id='1', email_verify=1)
        Student.objects.create(id = 2, stu_id='2', stu_name='2', email='2', password='2', wx_id='2', email_verify=1)
        Student.objects.create(id = 3, stu_id='3', stu_name='3', email='3', password='3', wx_id='3', email_verify=1)
        Student.objects.create(id = 4, stu_id='4', stu_name='4', email='4', password='4', wx_id='4', email_verify=1)
        Student.objects.create(id = 5, stu_id='5', stu_name='5', email='5', password='5', wx_id='5', email_verify=1)

        Building.objects.create(building_id=1, building_abbr='aa', building_name='aa', 
                                                building_desc='m', is_open=True, config_url='2', 
                                                longitude=31.54, latitude=121.27)
        Building.objects.create(building_id=2, building_abbr='bb', building_name='bb', 
                                                building_desc='s', is_open=True, config_url='2', 
                                                longitude=32.67, latitude=122.34)
        Building.objects.create(building_id=3, building_abbr='cc', building_name='cc', 
                                                building_desc='j', is_open=True, config_url='2', 
                                                longitude=31.86, latitude=121.89)
        
        Room.objects.create(room_id=1, room_number='1', room_desc='1', config_url='1',
                                                is_open=1, capacity=1, overnight=1, building_id_id=1)
        Room.objects.create(room_id=2, room_number='2', room_desc='2', config_url='2',
                                                is_open=1, capacity=1, overnight=1, building_id_id=2)
        Room.objects.create(room_id=3, room_number='3', room_desc='3', config_url='3',
                                                is_open=1, capacity=1, overnight=1, building_id_id=3)
        Room.objects.create(room_id=4, room_number='4', room_desc='4', config_url='4',
                                                is_open=1, capacity=1, overnight=1, building_id_id=1)
        Room.objects.create(room_id=5, room_number='5', room_desc='5', config_url='5',
                                                is_open=1, capacity=1, overnight=1, building_id_id=2)
        
        Seat.objects.create(seat_id=1, room_id_id=1, seat_number='1', x_position=1, y_position=1,
                                                is_open=1, is_with_plug=1, is_reserved=0)
        Seat.objects.create(seat_id=2, room_id_id=1, seat_number='2', x_position=2, y_position=2,
                                                is_open=1, is_with_plug=1, is_reserved=0)
        Seat.objects.create(seat_id=3, room_id_id=1, seat_number='3', x_position=3, y_position=3,
                                                is_open=1, is_with_plug=1, is_reserved=0)
        Seat.objects.create(seat_id=4, room_id_id=2, seat_number='4', x_position=4, y_position=4,
                                                is_open=1, is_with_plug=1, is_reserved=0)
        Seat.objects.create(seat_id=5, room_id_id=3, seat_number='5', x_position=5, y_position=5,
                                                is_open=1, is_with_plug=1, is_reserved=0)
        Seat.objects.create(seat_id=6, room_id_id=4, seat_number='6', x_position=6, y_position=6,
                                                is_open=1, is_with_plug=1, is_reserved=0)
        
        Reservation.objects.create(rsv_id=1, seat_id_id=1, stu_id_id=1, rsv_state='已预约',
                                                make_rsv_time='2023-04-01 09:00', start_rsv_time='2023-04-01 13:00',
                                                end_rsv_time='2023-04-01 16:00')
        Reservation.objects.create(rsv_id=2, seat_id_id=2, stu_id_id=2, rsv_state='已预约',
                                                make_rsv_time='2023-04-01 00:00', start_rsv_time='2023-04-01 06:00',
                                                end_rsv_time='2023-04-01 8:00')
        Reservation.objects.create(rsv_id=3, seat_id_id=3, stu_id_id=3, rsv_state='已预约',
                                                make_rsv_time='2023-04-01 09:00', start_rsv_time='2023-04-01 12:00',
                                                end_rsv_time='2023-04-01 15:00')
        Reservation.objects.create(rsv_id=4, seat_id_id=4, stu_id_id=4, rsv_state='已预约',
                                                make_rsv_time='2023-04-01 09:00', start_rsv_time='2023-04-01 09:00',   
                                                end_rsv_time='2023-04-01 13:00')
        Reservation.objects.create(rsv_id=5, seat_id_id=5, stu_id_id=5, rsv_state='已预约',
                                                make_rsv_time='2023-04-01 09:00', start_rsv_time='2023-04-01 09:00',
                                                end_rsv_time='2023-04-01 13:00')

        self.building_service = BuildingService()
        self.room_service = RoomService()
        self.seat_service = SeatService()
        self.stu_service = StudentService()
        self.reservation_service = ReservationService()

    def test_seat(self):
        self.assertEqual(self.seat_service.verify_seat_with_seat_id('1'), True)
        seat_list = self.seat_service.select_seats(1, '2023-04-01 09:00', '2023-04-01 13:00')
        self.assertEqual(seat_list[0]['seat_id'], 1)
        self.assertEqual(len(seat_list), 3)
        # print(seat_list)
        # self.assertEqual(seat_list[0]['is_reserved'], 0)
        # self.assertEqual(seat_list[1]['is_reserved'], 0)
        # self.assertEqual(seat_list[2]['is_reserved'], 1)

    def test_reservation(self):
        self.reservation_service.create_reservation(self.stu_service.select_student_with_stu_id(stu_id='1'), 6, '2023-04-01 15:00', '2023-04-01 18:00')
        self.assertEqual(self.reservation_service.verify_reservation_with_rsv_id(6), True)
        self.reservation_service.delete_reservation_with_rsv_id(6)
        self.assertEqual(self.reservation_service.verify_reservation_is_deletable(6), False)
        rsvs = self.reservation_service.select_reservation_and_sort(self.stu_service.select_student_with_stu_id(stu_id='1'))
        self.assertEqual(len(rsvs), 2)
        self.reservation_service.mark_as_waiting(Reservation.objects.get(rsv_id=3))
        self.assertEqual(Reservation.objects.get(rsv_id=3).rsv_state, '待签到')
        self.reservation_service.mark_as_signed(Reservation.objects.get(rsv_id=3))
        self.assertEqual(Reservation.objects.get(rsv_id=3).rsv_state, '已签到')
        self.reservation_service.mark_as_defaulted(Reservation.objects.get(rsv_id=3))
        self.assertEqual(Reservation.objects.get(rsv_id=3).rsv_state, '已违约')


    def tearDown(self):
        Student.objects.all().delete()
        Building.objects.all().delete()
        Room.objects.all().delete()
        Seat.objects.all().delete()
        Reservation.objects.all().delete()
        

        