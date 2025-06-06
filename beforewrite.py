import sensor, image, time
from machine import UART
import pyb
p3 = pyb.Pin('P3', pyb.Pin.OUT_PP)
p4 = pyb.Pin('P4', pyb.Pin.OUT_PP)
p5 = pyb.Pin('P5', pyb.Pin.OUT_PP)
p3.low()
p4.low()
p5.low()
black_threshold = (0, 21, -19, 0, -7, 26)
blue_threshold = (46, 90, -29, -4, -31, -11)
red_threshold =(0, 76, 14, 76, 2, 50)#red
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()
    left_blobs = img.find_blobs([black_threshold], roi=(0, 150, 100, img.height()-150))
    right_blobs = img.find_blobs([black_threshold], roi=(320-100, 150, 100   , img.height()-150))
    blue_blobs = img.find_blobs([blue_threshold],x_stride=50,y_stride=50)
    red_blobs = img.find_blobs([red_threshold], x_stride=50, y_stride=50)
    left_count = sum([blob.pixels() for blob in left_blobs])
    right_count = sum([blob.pixels() for blob in right_blobs])
    print(left_count,right_count)
    if blue_blobs:
        p3.high()
        p4.high()
    elif left_count>right_count:
        p3.high()
        p4.low()
    elif right_count>left_count:
        p3.low()
        p4.high()
    else:
        p3.low()
        p4.low()
    if red_blobs:
        # 取最大的红色物块
        largest_red_blob = max(red_blobs, key=lambda b: b.pixels())
        # 打印出最大红色物块的大小
        print('Red blob size:', largest_red_blob.pixels())
