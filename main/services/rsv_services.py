import time

import pytz
import datetime as date
from datetime import datetime
from time import *

from ..models import *

from django.core.mail import send_mail
import qrcode
from io import BytesIO

import math

from datetime import timedelta
from django.utils import timezone

from pyDes import des, PAD_PKCS5
import base64
import json

from decimal import Decimal

deskey = "mossssom"


def deg_to_rad(d):
    return d / 180 * math.pi


def distance(x1, y1, x2, y2):
    x1, y1, x2, y2 = deg_to_rad(float(x1)), deg_to_rad(float(y1)), deg_to_rad(float(x2)), deg_to_rad(float(y2))
    return 6371 * math.acos(math.sin(x1) * math.sin(x2) + math.cos(x1) * math.cos(x2) * math.cos(y1 - y2))


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class ReservationService:

    def create_reservation(self, student, seat_id, start_rsv_time, end_rsv_time):
        make_rsv_time = str(datetime.now())
        make_rsv_time = datetime.strptime(make_rsv_time[:-10], '%Y-%m-%d %H:%M')
        start_rsv_time = datetime.strptime(start_rsv_time, '%Y-%m-%d %H:%M')
        end_rsv_time = datetime.strptime(end_rsv_time, '%Y-%m-%d %H:%M')
        reservation = Reservation(seat_id_id=seat_id, stu_id_id=student['id'], rsv_state='已预约',
                                  make_rsv_time=make_rsv_time, start_rsv_time=start_rsv_time, end_rsv_time=end_rsv_time)
        reservation.save()
        seat = Seat.objects.get(seat_id=seat_id)
        seat.is_reserved = True
        seat.save()
        return {}

    def select_reservation_and_sort(self, student):
        r_list = Reservation.objects.filter(stu_id=student['id']). \
            values_list('rsv_id', 'rsv_state', 'seat_id_id', 'seat_id__seat_number',
                        'seat_id__room_id__building_id__building_name', 'seat_id__room_id__room_number',
                        'make_rsv_time', 'start_rsv_time', 'end_rsv_time')
        reservations = []
        now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
        for r in r_list:
            delta_time = now - r[7] if now > r[7] else r[7] - now
            reservations.append({'rsv_id': r[0], 'rsv_state': r[1], 'seat_id': r[2], 'seat_number': r[3],
                                 'building_name': r[4], 'room_number': r[5], 'make_rsv_time': r[6],
                                 'start_rsv_time': r[7], 'end_rsv_time': r[8], 'delta_time': delta_time})
        rsv_priority = {'已预约': 1, '待签到': 0, '已签到': 2, '已完成': 4, '已取消': 4, '已违约': 4}
        reservations.sort(key=lambda reservation: reservation['start_rsv_time'], reverse=False)
        reservations.sort(key=lambda reservation: rsv_priority[reservation['rsv_state']], reverse=False)
        return reservations

    def verify_reservation_with_rsv_id(self, rsv_id):
        return Reservation.objects.filter(rsv_id=rsv_id).exists()

    def delete_reservation_with_rsv_id(self, rsv_id):
        reservation = Reservation.objects.get(rsv_id=rsv_id)
        reservation.rsv_state = '已取消'
        reservation.save()
        seat = Seat.objects.get(seat_id=reservation.seat_id_id)
        seat.is_reserved = False
        seat.save()
        return {}

    def verify_reservation_is_deletable(self, rsv_id):
        make_del_time = datetime.now() + date.timedelta(minutes=15)
        make_del_time = make_del_time.replace(tzinfo=pytz.timezone('UTC'))
        reservation = Reservation.objects.filter.get(rsv_id=rsv_id)
        return reservation.start_rsv_time >= make_del_time

    ## 邮件提醒功能，用于前15分钟邮件提醒
    def send_reminder_as_email(self, reservation):
        # reservation = Reservation.objects.get(rsv_id = 1)
        subject = '图书馆自习室预约提醒'
        seat = Seat.objects.get(seat_id=reservation.seat_id_id)
        message = '您预约的座位' + seat.seat_number + '（' + str(reservation.start_rsv_time) + '~' + str(
            reservation.end_rsv_time) + '）即将开始，请在' + str(reservation.start_rsv_time) + '前签到。'
        from_email = 'gaishuangnht1@163.com'
        user = Student.objects.get(id=reservation.stu_id_id)
        send_mail(subject, message, from_email, [user.email])

    def mark_as_waiting(self, reservertion):
        new_reservertion = Reservation.objects.get(rsv_id=reservertion.rsv_id)
        new_reservertion.rsv_state = "待签到"
        new_reservertion.save()

    def mark_as_defaulted(self, reservertion):
        new_reservertion = Reservation.objects.get(rsv_id=reservertion.rsv_id)
        new_reservertion.rsv_state = "已违约"
        new_reservertion.save()
        seat = Seat.objects.get(seat_id=reservertion.seat_id_id)
        seat.is_reserved = False
        seat.save()

    def mark_as_signed(self, reservertion):
        new_reservertion = Reservation.objects.get(rsv_id=reservertion.rsv_id)
        new_reservertion.rsv_state = "已签到"
        new_reservertion.save()

    def generate_signin_code(self, seatid):
        data = {}
        seat = Seat.objects.get(seat_id=seatid)
        room = Room.objects.get(room_id=seat.room_id_id)
        building = Building.objects.get(building_id=room.building_id_id)
        data["seat_id"] = seatid
        data["seat_number"] = seat.seat_number
        data["latitude"] = building.latitude
        data["longitude"] = building.longitude
        json_str = json.dumps(data, cls=DecimalEncoder)
        return self.encrypt_des(deskey, json_str)

    def signin_verify(self, stu_id, signin_code, latitude, longitude):
        str = self.decrypt_des(deskey, signin_code)
        data = json.loads(str)
        print(data)
        if distance(data["latitude"], data["longitude"], latitude, longitude) > 0.5:
            return {'is_success': False, 'reasons': 'overdistance'}
        reservations = Reservation.objects.filter(stu_id_id=stu_id, seat_id_id=data["seat_id"], rsv_state="待签到")
        if reservations.count() == 0:
            return {'is_success': False, 'reasons': 'noReservation'}
        if reservations.count() != 1:
            return {'is_success': False, 'reasons': 'ReservationCountError'}
        if reservations[0].start_rsv_time - timedelta(minutes=15) <= timezone.now() <= reservations[0].start_rsv_time:
            return {'is_success': False, 'reasons': 'TimeError'}
        reservation = Reservation.objects.get(rsv_id=reservations[0].rsv_id)
        reservation.rsv_state = "已签到"
        reservation.save()
        return {'is_success': True, 'reasons': ''}

    def generate_qr_code(self, data):
        # 创建二维码对象
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L,
        )
        # 设置二维码的数据
        qr.add_data(data)
        qr.make(fit=True)

        # 生成图片
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # 创建一个字节流对象
        image_stream = BytesIO()
        qr_image.save(image_stream, 'PNG')

        return image_stream

    def encrypt_des(self, key, data):
        # 创建DES加密器
        cipher = des(key, padmode=PAD_PKCS5)
        # 使用加密器对数据进行加密
        encrypted_data = cipher.encrypt(data)
        # 对加密后的数据进行Base64编码
        encoded_data = base64.b64encode(encrypted_data)
        # 返回加密后的数据
        return encoded_data

    def decrypt_des(self, key, encrypted_data):
        # 创建DES解密器
        cipher = des(key, padmode=PAD_PKCS5)
        # 对Base64编码的密文进行解码
        decoded_data = base64.b64decode(encrypted_data)
        # 使用解密器对数据进行解密
        decrypted_data = cipher.decrypt(decoded_data)
        # 返回解密后的数据
        return decrypted_data
