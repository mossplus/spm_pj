from django.test import TestCase
from ..models import *
from ..services import BuildingService


# reference:
#  https://docs.djangoproject.com/en/4.2/topics/testing/overview/
#  https://docs.python.org/3/library/unittest.html#module-unittes


class BuildingTestCase(TestCase):
    def setUp(self):
        # self.ids = [dct['id'] for dct in Building.objects.values('id')]
        self.building = Building.objects.create(building_id='2', building_abbr='2', building_name='2', 
                                                building_desc='2', is_open=True, config_url='2', 
                                                longitude=2, latitude=2)
        self.building_service = BuildingService()

    def test_building(self):
        self.assertEqual(self.building_service.verify_building_with_building_id('2'), True)