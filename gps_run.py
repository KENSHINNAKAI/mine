import time
import board
import busio
import adafruit_bno055
import math
from readline import set_completion_display_matches_hook
from socket import MSG_WAITALL
import serial

# Use these lines for I2C
i2c = busio.I2C(board.GPIO3, board.GPIO2)
sensor = adafruit_bno055.BNO055_I2C(i2c)  #9軸加速度センサ
last_val = 0xFFFF

goal_place = [35.598939,139.651286] #goalの座標
#start_place =[a,b] #startの座標を取得
#rad_start = math.atan((139.651286- b)/(35.598939 - a)) #startからgoalの角度を求める
#print(rad_start) #角度を表示
l#ength_start = (start) #startからgoalの距離を求める
#print(length_start) #距離を表示
time = 0 #時間の初期化 
serial_tty = "/dev/ttyS0" #謎
serial_speed = 9600　#シリアル通信速度
ser = serial.Serial( serial_tty, serial_speed ) #シリアル系何か決めてる

def dm_to_deg( data ):
    deg = int ( float(data) / 100 )
    min = float( data ) - deg * 100
    return( round( deg + min / 60.0 , 6 ) )   #演算

def ntg(rad_ntg, long_dig): #距離を求める関数を定義
    distance = 0
    distance = (35.598939 - long_dig) /  math.cos(rad_ntg) 
    return(distance)

def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result      #温度を求める正直わからん

def rad_magnet(Magnatometor[0], Magnatometor[1])
   rad = 0
   rad = math.atan(Magnatometor[0] / Magnatometor[1])
return rad 



while (True):

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
        elevation =  float(gps_data[9]) - float(gps_data[11])
        
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

        

    now_place = [lat_dig,long_dig] #現在地の取得
    print(now_place) #現在地の表示
    rad_ntg = math.atan((139.651286- lat_dig)/(35.598939 - long_dig)) #nowからgoalまでの角度を求める
    deg_ntg = rad_ntg * 180 / math.pi() #ラジアンからdegに変換
    distance_ntg = ntg( rad_ntg, long_dig) #nowからgoalまでの距離を求める
    print(distance_ntg) #距離の表示
    while (time % 2 == 0): #2秒ごとにrad_ntgをrad_startと比較する
        if deg_ntg <= 5 || deg_ntg >= -5:
            #モーターを直進させる
        else
	#
            #モータを-5<deg_ntg<5になるまで回転させる    
    if now_place == goal_place: #nowがgoalと一致したときループを抜ける
        break
    time = time + 1
    print(time)
#モーターを止める



# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

