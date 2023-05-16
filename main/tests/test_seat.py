from django.test import TestCase
from ..models import *
from ..services import BuildingService, RoomService, SeatService, ReservationService

# reference:
#  https://docs.djangoproject.com/en/4.2/topics/testing/overview/
#  https://docs.python.org/3/library/unittest.html#module-unittes

class SeatTestCase(TestCase):
    def setUp(self):
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
        
        
        self.building_service = BuildingService()
        self.room_service = RoomService()
        self.seat_service = SeatService()
        self.reservation_service = ReservationService()

    def test_seat(self):
        self.assertEqual(self.seat_service.verify_seat_with_seat_id('1'), True)
        seat_list = self.seat_service.select_seats(1, '2023-04-01 09:00', '2023-04-01 13:00')
        self.assertEqual(seat_list[0]['seat_id'], 1)
        self.assertEqual(len(seat_list), 2)

    def test_reservation(self):
        pass

        