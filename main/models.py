from django.db import models


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    wx_id = models.CharField(max_length=256)
    stu_id = models.CharField(max_length=12, unique=True,null=True)
    stu_name = models.CharField(max_length=20,null=True)
    password = models.CharField(max_length=20,null=True)
    email = models.CharField(max_length=100)
    email_verify = models.BooleanField()


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    manager_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)


class Setting(models.Model):
    id = models.AutoField(primary_key=True)
    max_reserve_span = models.DecimalField(max_digits=4, decimal_places=2, default=4.00)
    start_reserve_time = models.TimeField()
    end_reserve_time = models.TimeField()


class Building(models.Model):
    building_id = models.AutoField(primary_key=True)
    building_abbr = models.CharField(max_length=10)
    building_name = models.CharField(max_length=15)
    building_desc = models.CharField(max_length=200)
    config_url = models.FileField(upload_to='media/configs/', null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    is_open = models.BooleanField(default=False)


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=20)
    building_id = models.ForeignKey('Building', to_field='building_id', on_delete=models.CASCADE)
    room_desc = models.CharField(max_length=200, null=True)
    config_url = models.FileField(upload_to='media/configs/', null=True)
    is_open = models.BooleanField(default=False)
    capacity = models.DecimalField(max_digits=4, decimal_places=0, default=150)
    overnight = models.BooleanField(default=False)


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey('Room', to_field='room_id', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=30)
    x_position = models.DecimalField(max_digits=10, decimal_places=6)
    y_position = models.DecimalField(max_digits=10, decimal_places=6)
    is_open = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    is_with_plug = models.BooleanField(default=False)


class Reservation(models.Model):
    rsv_id = models.AutoField(primary_key=True)
    stu_id = models.ForeignKey('Student', to_field='id', on_delete=models.CASCADE)
    seat_id = models.ForeignKey('Seat', to_field='seat_id', on_delete=models.CASCADE)
    rsv_state = models.CharField(max_length=20, null=False)
    make_rsv_time = models.DateTimeField()
    start_rsv_time = models.DateTimeField()
    end_rsv_time = models.DateTimeField()
