import os
import shutil

import math
import datetime as date
from datetime import datetime

from django.db.models import Sum, Count, Max, Min, Avg

from spm_pj.settings import BASE_DIR
from ..models import *


def deg_to_rad(d):
    return d / 180 * math.pi


def distance(x1, y1, x2, y2):
    x1, y1, x2, y2 = deg_to_rad(float(x1)), deg_to_rad(float(y1)), deg_to_rad(float(x2)), deg_to_rad(float(y2))
    return 6371 * math.acos(math.sin(x1) * math.sin(x2) + math.cos(x1) * math.cos(x2) * math.cos(y1 - y2))


def date_time_to_str(date_time):
    return (str(date_time).split('+'))[0][:-3]


def query_set_to_dict(query_set, key, value):
    if len(query_set) == 0:
        return {}
    return {query_set[i][key]: query_set[i][value] for i in range(len(query_set))}


class BuildingService:

    def select_buildings_and_sort(self, latitude, longitude):

        b_list = Building.objects.\
            values_list('building_id', 'building_abbr', 'building_name', 'building_desc',
                        'is_open', 'config_url', 'longitude', 'latitude')
        c_list = Room.objects.values('building_id_id').annotate(capacity=Sum('capacity'))
        r_list = Reservation.objects.filter(rsv_state__in=['已预约', '待签到', '已签到', ]).\
            values('seat_id__room_id__building_id_id').annotate(reserved=Count('rsv_id'))

        c_dict = query_set_to_dict(c_list, key='building_id_id', value='capacity')
        r_dict = query_set_to_dict(r_list, key='seat_id__room_id__building_id_id', value='reserved')
        assert len(b_list) == len(c_list)

        buildings = []
        for b in b_list:
            buildings.append({'building_id': b[0], 'building_abbr': b[1], 'building_name': b[2],
                              'building_desc': b[3], 'is_open': b[4], 'config_url': str(b[5]),
                              'distance': distance(b[7], b[6], latitude, longitude),
                              'capacity': int(c_dict[b[0]]), 'reserved': int(r_dict[b[0]]) if b[0] in r_dict else 0})
        buildings.sort(key=lambda building: building['distance'], reverse=False)
        return buildings

    def verify_building_with_building_id(self, building_id):
        return Building.objects.filter(building_id=building_id).exists()

    def select_building_with_building_id(self, building_id, latitude, longitude):
        building = Building.objects.get(building_id=building_id)
        return {'building_id': building.building_id, 'building_abbr': building.building_abbr,
                'building_name': building.building_name, 'building_desc': building.building_desc,
                'is_open': building.is_open, 'config_url': str(building.config_url),
                'distance': distance(building.latitude, building.longitude, latitude, longitude)}


class RoomService:

    def select_rooms_and_sort(self, building_id):

        c_list = Room.objects.filter(building_id=building_id).\
            values_list('room_id', 'room_number', 'room_desc', 'is_open', 'config_url', 'capacity', 'overnight')
        r_list = Reservation.objects.filter(seat_id__room_id__building_id_id=building_id,
                                            rsv_state__in=['已预约', '待签到', '已签到', ]). \
            values('seat_id__room_id_id').annotate(reserved=Count('rsv_id'))

        r_dict = query_set_to_dict(r_list, key='seat_id__room_id_id', value='reserved')

        rooms = []
        for c in c_list:
            rooms.append({'room_id': c[0], 'room_number': c[1], 'room_desc': c[2],
                          'is_open': c[3], 'config_url': str(c[4]), 'overnight': c[6],
                          'capacity': int(c[5]), 'reserved': int(r_dict[c[0]]) if c[0] in r_dict else 0})
        rooms.sort(key=lambda room: room['room_id'])
        return rooms

    def verify_room_with_room_id(self, room_id):
        return Room.objects.filter(room_id=room_id).exists()

    def select_room_with_room_id(self, room_id):
        room = Room.objects.get(room_id=room_id)
        return {'room_id': room.room_id, 'room_number': room.room_number, 'room_desc': room.room_desc,
                'building_id': room.building_id_id, 'is_open': room.is_open, 'config_url': str(room.config_url),
                'capacity': int(room.capacity), 'overnight': room.overnight}


class SeatService:

    def select_seats(self, room_id, start_time, end_time):

        s_list = Seat.objects.filter(room_id=room_id).\
            values_list('seat_id', 'seat_number', 'x_position', 'y_position', 'is_open', 'is_with_plug')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
        re_lst = Reservation.objects.filter(seat_id__room_id_id=room_id, start_rsv_time__lt=end_time,
                                            rsv_state__in=['已预约', '待签到', '已签到', ]).values('seat_id_id')
        re_lst = [r['seat_id_id'] for r in re_lst]
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        rs_lst = Reservation.objects.filter(seat_id__room_id_id=room_id, end_rsv_time__gt=start_time,
                                            rsv_state__in=['已预约', '待签到', '已签到', ]).values('seat_id_id')
        rs_lst = [r['seat_id_id'] for r in rs_lst]

        seats = []
        for s in s_list:
            seats.append({'seat_id': s[0], 'seat_number': s[1], 'x_position': float(s[2]), 'y_position': float(s[3]),
                          'is_open': s[4], 'is_with_plug': s[5], 'is_reserved': s[0] in rs_lst or s[0] in re_lst})
        return seats

    def verify_seat_with_seat_id(self, seat_id):
        return Seat.objects.filter(seat_id=seat_id).exists()

