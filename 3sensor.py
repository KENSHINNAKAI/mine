from time import sleep
import LPS25HB
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055
import serial

# LPS25HBが検出されるかどうか確認
sleep(0.1)
if (LPS25HB.LPS_init() == False):
    print("Failed to autodetect pressure sensor!")
    while (True):
        sleep(0.1)
        
LPS25HB.enableDefault()

# Use these lines for I2C
i2c = I2C(1)  # Device is /dev/i2c-1
sensor = adafruit_bno055.BNO055_I2C(i2c)


last_val = 0xFFFF

def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


serial_tty = "/dev/ttyS0"
serial_speed = 9600

ser = serial.Serial( serial_tty, serial_speed )


while True:
    print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    print("Euler angle: {}".format(sensor.euler))
    print("Quaternion: {}".format(sensor.quaternion))
    print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    print("Gravity (m/s^2): {}".format(sensor.gravity))
    print()

    pressure = LPS25HB.readPressureMillibars()
    altitude = LPS25HB.pressureToAltitudeMeters(pressure)
    temperature = LPS25HB.readTemperatureC()
  
    print("p:",round(pressure,2),"tmbar a:",round(altitude,2),"mttt:",round(temperature,2),"deg C ")
    print()

    gps_line = ''
    while ( True ):
        buf = ser.read()
        if ( buf == b'\r' ):
            break
        elif ( buf != b'\n' ):
            gps_line = gps_line + buf.decode()
    print( gps_line )


    sleep(1)