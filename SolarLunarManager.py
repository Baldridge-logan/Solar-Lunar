#from SolarLunarData import CelestialData
from SolarLunarMotors import MotorController
import time
# HoustonMachine = CelestialData("Houston, TX")
# sun_data = HoustonMachine.fetch_data("Sun", 1)
# moon_data = HoustonMachine.fetch_data("Moon", 1)

BOTTOM_HAT_ADDR = 0x60
TOP_HAT_ADDR = 0x61

inner_base_stepper = MotorController(BOTTOM_HAT_ADDR, 1, 8) #port 1 = M1 & M2
outer_base_stepper = MotorController(BOTTOM_HAT_ADDR, 2, 8) #port 2 = M3 & M4

inner_spool_stepper = MotorController(TOP_HAT_ADDR, 1, 58) #port 1 = M1 & M2
outer_spool_stepper = MotorController(TOP_HAT_ADDR, 2, 58) #port 2 = M3 & M4

#outer_base_stepper.set_direction("CW")
#outer_base_stepper.move_degrees(1,100)

for num in range(3):
	inner_spool_stepper.set_direction("UP")
	inner_spool_stepper.move_degrees(30+15*num, 10)
	#inner_base_stepper.move_degrees(360, 100)
	time.sleep(4)

	inner_spool_stepper.set_direction("DOWN")
	inner_spool_stepper.move_degrees(30+15*num, 10)
	time.sleep(4)
