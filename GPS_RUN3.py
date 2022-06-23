from multiprocessing.connection import wait
import time
import board
import busio
import adafruit_bno055
import math
from readline import set_completion_display_matches_hook
from socket import MSG_WAITALL
import serial
from tokenize import Double
from adafruit_extended_bus import ExtendedI2C as I2C
from geopy.distance import geodesic
import RPi.GPIO as GPIO

THRESHOLD = 15
right_front=23
left_front=25
right_back=24
left_back=8

GPIO.setmode(GPIO.BCM)
GPIO.setup(right_front,GPIO.OUT)
GPIO.setup(left_front,GPIO.OUT)
GPIO.setup(right_back,GPIO.OUT)
GPIO.setup(left_back,GPIO.OUT)

GPIO.setwarnings(False)

def forward(x):
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    time.sleep(x)
    return()

def back(x):
    GPIO.output(right_back,GPIO.HIGH)
    GPIO.output(left_back,GPIO.HIGH)
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.LOW)
    time.sleep(x)
    return()

def leftturn(x):
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.LOW)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.HIGH)
    time.sleep(x)
    return()

def rightturn(x):
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.HIGH)
    GPIO.output(left_back,GPIO.LOW)
    time.sleep(x)
    return()

def reforward(x):#back and forward
    GPIO.output(right_back,GPIO.HIGH)
    GPIO.output(left_back,GPIO.HIGH)
    GPIO.output(right_front,GPIO.LOW)
    GPIO.output(left_front,GPIO.LOW)
    time.sleep(x)
    GPIO.output(right_front,GPIO.HIGH)
    GPIO.output(left_front,GPIO.HIGH)
    GPIO.output(right_back,GPIO.LOW)
    GPIO.output(left_back,GPIO.LOW)
    time.sleep(5)

def wave(x):#continuous back and forward
    for i in range(x):
        GPIO.output(right_back,GPIO.HIGH)
        GPIO.output(left_back,GPIO.HIGH)
        GPIO.output(right_front,GPIO.LOW)
        GPIO.output(left_front,GPIO.LOW)
        time.sleep(1)
        GPIO.output(right_front,GPIO.HIGH)
        GPIO.output(left_front,GPIO.HIGH)
        GPIO.output(right_back,GPIO.LOW)
        GPIO.output(left_back,GPIO.LOW)
        time.sleep(1)
        

(goal_x, goal_y)= (35.7289,139.710223)
goal_place = (goal_x, goal_y)
# Use these lines for I2C
i2c = I2C(1)  # Device is /dev/i2c-1
sensor = adafruit_bno055.BNO055_I2C(i2c)
last_val = 0xFFFF


serial_tty = "/dev/ttyS0" #謎
serial_speed = 9600 #シリアル通信速度
ser = serial.Serial( serial_tty, serial_speed ) #シリアル系何か決めてる

def dm_to_deg( data ):
    deg = int ( float(data) / 100 )
    min = float( data ) - deg * 100
    return( round( deg + min / 60.0 , 6 ) )   #演算


def rad_magnet(mag_x, mag_y):
    rad = 0
    rad = math.atan2(mag_x , mag_y)
    return rad 

time_s = 0

while (True):
    print("")
    print("----------------------------------------------")
    print("")
    gps_line = ''
    while ( True ):
        buf = ser.read()
        if ( buf == b'\r' ):
            break
        elif ( buf != b'\n' ):
            gps_line = gps_line + buf.decode()

    gps_data = gps_line.split(",")
    if ( gps_data[0] == '$GPGGA' ): 
        when = gps_data[1]
        lat = gps_data[2]
        long = gps_data[4]
        try:
            elevation =  float(gps_data[9]) - float(gps_data[11])
        except:
            pass
            print("GPS data are NULL")
        
        if ( lat != "" and long != "" ):
            oclock = when[0:2]
            minutes = when[2:4]
            second = when[4:8]
            lat_deg = dm_to_deg( lat )
            long_deg = dm_to_deg( long )
            print ( "Latitude:", lat_deg , "  Longitude:", long_deg, "  Elevation:" , round(elevation,1) , "m" )
            print ( oclock, "時 ", minutes, "分 ", second, "秒")
        else:
            print ( "Cannot catch satellite radio." )
            print ( gps_line )



    now_place = (lat_deg,long_deg) #現在地の取得
    print(now_place) #現在地の表示
    rad_ntg = math.atan2((goal_y- lat_deg), (goal_x - long_deg)) #nowからgoalまでの角度を求める
    float(rad_ntg)
    deg_ntg = rad_ntg * 180 / math.pi #ラジアンからdegに変換
    float(deg_ntg)
    if deg_ntg<0:
         deg_ntg = deg_ntg + 360
         print(deg_ntg)
    else:
         print(deg_ntg)
    distance_ntg = geodesic(goal_place, now_place).m#nowからgoalまでの距離を求める
    print(distance_ntg) #距離の表示 
    
    [mag_x, mag_y, mag_z] = sensor.magnetic
    arg_degree = rad_magnet(mag_x, mag_y) * 180 / math.pi
    if arg_degree<0:
         arg_degree = arg_degree + 360
         print(arg_degree)
    else:
         print(arg_degree)

   
    
    if(time_s % 2 == 0): #2秒ごとにrad_ntgをrad_startと比較する
        if deg_ntg >= 0 and deg_ntg < THRESHOLD:
            if arg_degree <= (deg_ntg + THRESHOLD) and arg_degree >= (360 - deg_ntg):
                #forward(5)
                #モーターを直進させる
                print("foward")
            elif arg_degree <= (deg_ntg + 180) and arg_degree > (deg_ntg + THRESHOLD):
                rightturn(2)
                #モーターを右回転させる 
                print("rightturn")
            else:
                leftturn(2)
                #モーターを左回転させる
                print("leftturn")
        elif deg_ntg >= THRESHOLD and deg_ntg < 180:  
            if arg_degree <= (deg_ntg + THRESHOLD) and arg_degree >= (deg_ntg - THRESHOLD):
                #forward(5)
                #モーターを直進させる
                print("foward")
            elif arg_degree <= (deg_ntg + 180) and arg_degree > (deg_ntg + THRESHOLD):
                rightturn(2)
                #モーターを右回転させる 
                print("rightturn")
            else:
                leftturn(2)
                #モーターを左回転させる
                print("leftturn")
        elif deg_ntg >= 180 and deg_ntg < (360 - THRESHOLD):
            if arg_degree <= (deg_ntg + THRESHOLD) and arg_degree >= (deg_ntg - THRESHOLD):
                #forward(5)
                #モーターを直進させる
                print("foward")
            elif arg_degree <= (deg_ntg - THRESHOLD) and arg_degree > (deg_ntg - 180):
                leftturn(2)
                #モーターを左回転させる 
                print("leftturn")
            else:
                rightturn(2)
                #モーターを右回転させる
                print("rightturn")
        elif deg_ntg >= (360 - THRESHOLD) and deg_ntg < 360:
            if arg_degree <= (360 - deg_ntg) and arg_degree >= (deg_ntg - THRESHOLD):
                #forward(5)
                #モーターを直進させる
                print("foward")
            elif arg_degree <= (deg_ntg - THRESHOLD) and arg_degree > (deg_ntg - 180):
                leftturn(2)
                #モーターを左回転させる 
                print("leftturn")
            else:
                rightturn(2)
                #モーターを右回転させる
                print("rightturn")        
    if now_place == goal_place: #nowがgoalと一致したときループを抜ける
        break
    time_s = time_s + 1
    time.sleep(1)
    print(time_s)
#モーターを止める



# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT