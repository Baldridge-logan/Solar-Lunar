#from SolarLunarData import CelestialData
from SolarLunarMotors import MotorController
import time
import ephem
#HoustonMachine = CelestialData("Houston, TX")
#sun_data = HoustonMachine.fetch_data("Sun", 1)
#moon_data = HoustonMachine.fetch_data("Moon", 1)

BOTTOM_HAT_ADDR = 0x60
TOP_HAT_ADDR = 0x61

inner_base_stepper = MotorController(BOTTOM_HAT_ADDR, 2, 1) #port 1 = M1 & M2
outer_base_stepper = MotorController(BOTTOM_HAT_ADDR, 1, 1) #port 2 = M3 & M4

inner_spool_stepper = MotorController(TOP_HAT_ADDR, 2, 58) #port 1 = M1 & M2
outer_spool_stepper = MotorController(TOP_HAT_ADDR, 1, 87) #port 2 = M3 & M4

sun = ephem.Sun()
moon = ephem.Moon()

houston = ephem.Observer()
houston.lat = '29.7604'
houston.lon = '-95.3698'

sun.compute(houston)
moon.compute(houston)
pi = 3.14159265358
"""
print 'sun base'
outer_base_stepper.move_degrees(sun.az*180/pi,100)

print 'sun spool'
outer_spool_stepper.move_degrees(sun.alt*180/pi,10)
"""
print 'moon base'
inner_base_stepper.move_degrees(moon.az*180/pi,100)
print 'moon spool'
inner_spool_stepper.move_degrees(moon.alt*180/pi,10)

print sun.az , sun.alt , moon.az , moon.alt

sunaz = sun.az
moonaz = moon.az
sunalt = sun.alt
moonalt = moon.alt
time.sleep(3)

for num in range(1440):
    houston.date = ephem.now()*1.0+ephem.minute*num
    sun.compute(houston)#update sun and moon positions
    moon.compute(houston)
    
    sunaz_delta   = sun.az - sunaz#find changes
    moonaz_delta  = moon.az - moonaz
    sunalt_delta  = sun.alt - sunalt
    moonalt_delta = moon.alt - moonalt

    #print sunaz_delta , sunalt_delta
    print moon.alt, moon.az

    inner_spool_stepper.move_degrees(moonalt_delta*180/pi,10)
    inner_base_stepper.move_degrees(moonaz_delta*180/pi,100)
    
    sunaz   = sun.az
    moonaz  = moon.az
    sunalt  = sun.alt
    moonalt = moon.alt
    
    


#outer_base_stepper.set_direction("CW")
#outer_base_stepper.move_degrees(1,100)
"""
for num in range(3):
	#inner_spool_stepper.set_direction("UP")
	#inner_spool_stepper.move_degrees(30+15*num, 10)
	outer_base_stepper.move_degrees(-90, 100)
	time.sleep(4)

	#inner_spool_stepper.set_direction("DOWN")
	#inner_spool_stepper.move_degrees(30+15*num, 10)
	
"""
