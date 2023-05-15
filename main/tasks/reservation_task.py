from datetime import timedelta
from django.utils import timezone
from ..models import Reservation
from ..services.rsv_services import ReservationService
from django.db.models import Q

def check_reservations():
    # 获取所有还未确认的预约
    reservations = Reservation.objects.filter(rsv_state='已预约')
    reservationService = ReservationService()
    for reservation in reservations:
        # 如果预约时间前15分钟，发送提醒
        if reservation.start_rsv_time - timedelta(minutes=15) <= timezone.now() <= reservation.start_rsv_time:
            reservationService.mark_as_waiting(reservation)
            reservationService.send_reminder_as_email(reservation)
            print("["+timezone.now().strftime("%Y-%m-%d %H:%M:%S")+"]check_reservations: notification for email")

    # 如果预约时间后15分钟，将状态更改为违约
    reservations = Reservation.objects.filter(rsv_state='待签到')
    for reservation in reservations:
        if reservation.start_rsv_time + timedelta(minutes=15) < timezone.now():
            reservationService.mark_as_defaulted(reservation)
            print("["+timezone.now().strftime("%Y-%m-%d %H:%M:%S")+"]check_reservations: default record")
