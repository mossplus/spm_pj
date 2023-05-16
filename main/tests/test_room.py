from django.test import TestCase
from ..models import *
from ..services import BuildingService
import math

# reference:
#  https://docs.djangoproject.com/en/4.2/topics/testing/overview/
#  https://docs.python.org/3/library/unittest.html#module-unittes

def deg_to_rad(d):
    return d / 180 * math.pi


def distance(x1, y1, x2, y2):
    x1, y1, x2, y2 = deg_to_rad(float(x1)), deg_to_rad(float(y1)), deg_to_rad(float(x2)), deg_to_rad(float(y2))
    return 6371 * math.acos(math.sin(x1) * math.sin(x2) + math.cos(x1) * math.cos(x2) * math.cos(y1 - y2))

# 测试楼宇距离排序是否正确
class BuildingTestCase(TestCase):
    def setUp(self):
        # self.ids = [dct['id'] for dct in Building.objects.values('id')]
        self.building = Building.objects.create(building_id='1', building_abbr='aa', building_name='aa', 
                                                building_desc='m', is_open=True, config_url='2', 
                                                longitude=2, latitude=2)
        self.building = Building.objects.create(building_id='2', building_abbr='bb', building_name='bb', 
                                                building_desc='s', is_open=True, config_url='2', 
                                                longitude=2, latitude=2)
        self.building = Building.objects.create(building_id='3', building_abbr='cc', building_name='cc', 
                                                building_desc='j', is_open=True, config_url='2', 
                                                longitude=2, latitude=2)
        self.building_service = BuildingService()

    def test_building(self):
        self.assertEqual(self.building_service.verify_building_with_building_id('1'), True)