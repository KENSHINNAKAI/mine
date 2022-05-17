import lps25hb
from time import sleep

sleep(0.1)
if (lps25hb.LPS_init() == False):
    print("Failed to autodetect pressure sensor!")
    while (True):
        sleep(0.1)
        
lps25hb.enableDefault()
while(True):
    pressure = lps25hb.readPressureMillibars()
    altitude = lps25hb.pressureToAltitudeMeters(pressure)
    temperature = lps25hb.readTemperatureC()
  
    print("p:",round(pressure,2),"tmbar a:",round(altitude,2),"mttt:",round(temperature,2),"deg C ")
    sleep(0.1)