from readline import set_completion_display_matches_hook
from socket import MSG_WAITALL
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
        when = gps_data[1]
        lat = gps_data[2]
        long = gps_data[4]
        #velocity_knot = gps_data[7]
        #direction = gps_data[8]
        elevation =  float(gps_data[9]) - float(gps_data[11])
        
        if ( lat != "" and long != "" ):
            oclock = when[0:2]
            minutes = when[2:4]
            second = when[4:8]
            lat_deg = dm_to_deg( lat )
            long_deg = dm_to_deg( long )
            #velocity_m_s = velocity_knot * 0.5144
            #velocity_km_h = velocity_knot * 0.5144 * 3.600
            print ( "Latitude:", lat_deg , "  Longitude:", long_deg, "  Elevation:" , round(elevation,1) , "m" )
            print ( oclock, "時 ", minutes, "分 ", second, "秒")
            #print ( "方向:", direction,"度 速度(m/s):", velocity_m_s, "m/s 速度(km/h):", velocity_km_h, "km/h")
        else:
            print ( "Cannot catch satellite radio." )
            print ( gps_line )