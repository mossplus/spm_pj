# 设计说明

## 后端数据库交互（services）

（有空补充）


## 后端测试说明（tests）

（有空补充）

## 后端小程序交互（views）

### http://10.176.40.151:31115/login

**get 请求**：

1. 直接返回 JsonResponse(status='405', data={}, error='Method Not Allowed')

**post 请求**：需要获取 "stu_id" 学号，"password" 密码（可能有待调整）

1. 正确登录返回 APIResponse(status='200', data=student, error='') 
```json
  {"id": "主键", "wx_id": "微信号", "stu_id": "学号", "stu_name": "姓名"}
```
2. 密码错误 APIResponse(status='401', data={}, error='Invalid username or password')
3. 用户不存在 APIResponse(status='401', data={}, error='No this user')
4. 报错返回 APIResponse(status='500', data={}, error=e)

### http://10.176.40.151:31115/register

**get 请求**：

1. 直接返回 JsonResponse(status='405', data={}, error='Method Not Allowed')

**post 请求**：需要获取 "wx_id" 微信号（必须），"stu_id" 学号，"email" 邮箱，"stu_name" 学生姓名，"password" 密码

1. 首次申请注册返回 APIResponse(status='201', data={}, error='') 
2. 填写信息成功返回 APIResponse(status='200', data={}, error='')
3. 报错返回 APIResponse(status='500', data={}, error=e)

### http://10.176.40.151:31115/stu_index/str:stu_id/

**get 请求**：需要获取 "latitude" 纬度，"longitude" 经度

1. 用户正确返回 APIResponse(status='200', data={'student': student, 'buildings': buildings}, error='')
```json
{
  "student": {"id": "主键", "wx_id": "微信号", "stu_id": "学号", "stu_name": "姓名"}, 
  "buildings": [{"building_id": "楼宇主键", "building_abbr": "楼宇编号", "building_name": "楼宇名称", 
    "building_desc": "楼宇描述", "is_open": "是否开放", "config_url": "楼宇外景图",
    "distance": "楼宇距离", "capacity": "楼宇总容量", "reserved": "楼宇总预约量"}]
}
```
2. 用户不存在 APIResponse(status='401', data={}, error='No this user')
3. 报错返回 APIResponse(status='500', data={}, error=e)

**post 请求**

1. 直接返回 JsonResponse(status='405', data={}, error='Method Not Allowed')

### http://10.176.40.151:31115/stu_room/str:stu_id/str:building_id/

**get 请求**：需要获取 "latitude" 纬度，"longitude" 经度

1. 正确返回 APIResponse(status='200', data={'student': student, 'building': building, 'rooms': rooms}, error='')
```json
{
  "student": {"id": "主键", "wx_id": "微信号", "stu_id": "学号", "stu_name": "姓名"}, 
  "building": {"building_id": "楼宇主键", "building_abbr": "楼宇编号", "building_name": "楼宇名称", 
    "building_desc": "楼宇描述", "is_open": "是否开放", "config_url": "楼宇外景图", "distance": "楼宇距离"}, 
  "rooms": [{"room_id": "自习室主键", "room_number": "自习室编号", "overnight": "是否通宵自习室", 
    "room_desc": "自习室描述", "is_open": "是否开放", "config_url": "自习室布局",
    "capacity": "自习室容量", "reserved": "自习室预约量"}]
}
```
2. 楼宇不存在 APIResponse(status='404', data={}, error='No this building')
3. 用户不存在 APIResponse(status='401', data={}, error='No this user')
4. 报错返回 APIResponse(status='500', data={}, error=e)

**post 请求**：

1. 直接返回 JsonResponse(status='405', data={}, error='Method Not Allowed')

### http://10.176.40.151:31115/stu_seat/str:stu_id/str:room_id/

**get 请求**：

1. 正确返回 APIResponse(status='200', data={'student': student, 'room': room, 'seats': seats}, error='')
```json
{
  "student": {"id": "主键", "wx_id": "微信号", "stu_id": "学号", "stu_name": "姓名"}, 
  "room": {"room_id": "自习室主键", "room_number": "自习室编号", "building_id": "楼宇主键", "overnight": "是否通宵自习室", 
    "room_desc": "自习室描述", "is_open": "是否开放", "config_url": "自习室布局", "capacity": "自习室容量"},
  "seats": [{"seat_id": "座位主键", "seat_number": "座位编号", "x_position": "座位横坐标", "y_position": "作为纵坐标", 
    "is_open": "是否开放", "is_reserved": "是否有约", "is_with_plug": "是否有插头"}]
}
```
2. 自习室不存在 APIResponse(status='404', data={}, error='No this classroom')
3. 用户不存在 APIResponse(status='401', data={}, error='No this user')
4. 报错返回 APIResponse(status='500', data={}, error=e)

**post 请求**：需要获取 "seat_id" 座位主键，"start_rsv_time" 预约开始时间，"end_rsv_time" 预约结束时间

1. 成功预约返回 APIResponse(status='201', data={}, error='')
2. 座位不存在 APIResponse(status='404', data={}, error='No this seat')
3. 自习室不存在 APIResponse(status='404', data={}, error='No this classroom')
4. 用户不存在 APIResponse(status='401', data={}, error='No this user')
5. 报错返回 APIResponse(status='500', data={}, error=e)

### http://10.176.40.151:31115/stu_record/str:stu_id/

**get 请求**：

1. 正确返回 APIResponse(status='200', data={'student': student, 'reservation': reservation}, error='')
```json
{
  "student": {"id": "主键", "wx_id": "微信号", "stu_id": "学号", "stu_name": "姓名"}, 
  "reservations": [{"rsv_id": "主键", "rsv_state": "预约状态", "seat_id": "座位主键", "seat_number": "座位编号", 
    "building_name": "楼宇编号", "room_number": "房间编号", "make_rsv_time": "预约时间", 
    "start_rsv_time": "预约开始时间", "end_rsv_time": "预约结束时间", "delta_time": "距离预约开始剩余时间"}]
}
```
2. 用户不存在 APIResponse(status='401', data={}, error='No this user')
3. 报错返回 APIResponse(status='500', data={}, error=e)

**post 请求**：需要获取 "rsv_id" 预约主键

1. 成功取消返回 APIResponse(status='204', data={}, error='')
2. 预约不存在 APIResponse(status='404', data={}, error='No this reservation')
3. 用户不存在 APIResponse(status='401', data={}, error='No this user')
4. 报错返回 APIResponse(status='500', data={}, error=e)

### http://10.176.40.151:31115/qrcode/str:seat_id

**get 请求**：返回该座位id对应的二维码

### http://10.176.40.151:31115/signin

**get 请求**：

1. 直接返回 JsonResponse(status='405', data={}, error='Method Not Allowed')

**post 请求**：需要获取 "stu_id" 当前学生的id，"signin_code" 二维码扫描出的结果字符串，"latitude" 当前学生坐标纬度，"longitude" 当前学生坐标经度

1. 正确签到返回 APIResponse(status='200', data=data, error='')
```json
{
  "is_success": "是否签到成功", "reasons": "签到成功或失败原因"
}
```
 - 注：data中，"is_success判断签到是否成功"，若成功则"reasons"为空，表示学生已完成签到；若失败，则"reasons"里会写明具体原因，现在定义以下原因
   - "overdistance"：超出500m距离
   - "noReservation"：没有查询到预约
   - "ReservationCountError"：预约数量错误
   - "TimeError"：不在预约点前后15分钟
