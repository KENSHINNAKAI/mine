import serial

serial_tty = "/dev/ttyS0"
serial_speed = 9600

ser = serial.Serial( serial_tty, serial_speed )

while(True):
    gps_line = ''
    while ( True ):
        buf = ser.read()
        if ( buf == b'\r' ):
            break
        elif ( buf != b'\n' ):
            gps_line = gps_line + buf.decode()
    print( gps_line )
    

