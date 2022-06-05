import serial

serial_tty = "/dev/ttyS0"
serial_speed = 9600

ser = serial.Serial( serial_tty, serial_speed )

def dm_to_deg( data ):
    deg = int ( float(data) / 100 )
    min = float( data ) - deg * 100
    return( round( deg + min / 60.0 , 6 ) )

while(True):
    gps_line = ''
    while ( True ):
        buf = ser.read()
        if ( buf == b'\r' ):
            break
        elif ( buf != b'\n' ):
            gps_line = gps_line + buf.decode()
        
    gps_data = gps_line.split(",")
    if ( gps_data[0] == '$GPGGA' ):
        lat = gps_data[2]
        long = gps_data[4]
        elevation =  float(gps_data[9]) - float(gps_data[11])
        
        if ( lat != "" and long != "" ):
            lat_deg = dm_to_deg( lat )
            long_deg = dm_to_deg( long )
            print ( "Latitude:", lat_deg , "  Longitude:", long_deg, "  Elevation:" , round(elevation,1) , "m" )
        else:
            print ( "Cannot catch satellite radio." )
            print ( gps_line )


