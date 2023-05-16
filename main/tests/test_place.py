from django.test import TestCase
from ..models import *
from ..services import BuildingService, RoomService
import math

# reference:
#  https://docs.djangoproject.com/en/4.2/topics/testing/overview/
#  https://docs.python.org/3/library/unittest.html#module-unittes

def deg_to_rad(d):
    return d / 180 * math.pi


def distance(x1, y1, x2, y2):
    x1, y1, x2, y2 = deg_to_rad(float(x1)), deg_to_rad(float(y1)), deg_to_rad(float(x2)), deg_to_rad(float(y2))
    return 6371 * math.acos(math.sin(x1) * math.sin(x2) + math.cos(x1) * math.cos(x2) * math.cos(y1 - y2))


class PlaceTestCase(TestCase):
    def setUp(self):
        # self.ids = [dct['id'] for dct in Building.objects.values('id')]
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
        self.stu_longitude = 31.84
        self.stu_latitude = 121.21

    def test_building(self):
        self.assertEqual(self.building_service.verify_building_with_building_id('1'), True)
        building_1 = self.building_service.select_building_with_building_id('1', 
                                                                self.stu_latitude , self.stu_longitude)
        building_2 = self.building_service.select_building_with_building_id('2',          
                                                                self.stu_latitude , self.stu_longitude)
        building_3 = self.building_service.select_building_with_building_id('3',
                                                                self.stu_latitude , self.stu_longitude)
        dist = []
        dist.append(building_1['distance'])
        dist.append(building_2['distance'])
        dist.append(building_3['distance'])
        dist.sort()
        dist_sort = self.building_service.select_buildings_and_sort(self.stu_latitude , self.stu_longitude)
        self.assertEqual(dist[0], dist_sort[0]['distance'])
        self.assertEqual(dist[1], dist_sort[1]['distance'])
        self.assertEqual(dist[2], dist_sort[2]['distance'])

    def test_room(self):
        self.assertEqual(self.room_service.verify_room_with_room_id('1'), True)
        self.assertEqual(self.room_service.select_room_with_room_id('1')['room_id'], 1)
        room_set = self.room_service.select_rooms_and_sort('1')
        self.assertEqual(room_set[0]['room_id'], 1)
        self.assertEqual(room_set[1]['room_id'], 4)

    def tearDown(self):
        buildings = Building.objects.all()
        rooms = Room.objects.all()
        buildings.delete()
        rooms.delete()
        