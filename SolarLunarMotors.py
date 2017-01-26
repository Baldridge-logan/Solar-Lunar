from AdafruitLibrary import Adafruit_MotorHAT, Adafruit_StepperMotor
import sched, time

MOTOR_STEPS = 200
TOTAL_DEGREES = 360
MILLISECOND = .001

class MotorController:
	def __init__(self, hat_addr, motor_port, gear_ratio):
		self._stepper = Adafruit_MotorHAT(addr=hat_addr).getStepper(MOTOR_STEPS, motor_port)
		self.partial_steps = 0
		self.motor_direction = Adafruit_MotorHAT.FORWARD
		self.motor_mode = Adafruit_MotorHAT.SINGLE
		self.motor_ratio = gear_ratio
		self.tick_num = 0

	def set_direction(self, direction):
		if direction == "UP" or direction == "CCW":
			self.motor_direction = Adafruit_MotorHAT.BACKWARD
		elif direction == "DOWN" or direction == "CW":
			self.motor_direction = Adafruit_MotorHAT.FORWARD
		else:
			raise Exception("Invalid direction specified")

	def ticker(self):
		self.tick_num += 1
		print 'tick num =', self.tick_num
		self._stepper.oneStep(
			self.motor_direction, 
			self.motor_mode
		)

	def move_degrees(self, degrees, time_per_tick):
		"""
		Degrees argument corresponds to angle on physical arc
		Time per Tick is in milliseconds
		"""
		arc_proportion = degrees / float(TOTAL_DEGREES)
		delta_steps = (arc_proportion * MOTOR_STEPS) * self.motor_ratio

		self.partial_steps += (delta_steps % 1) #get overflow of delta
		true_delta_steps = int(delta_steps) + int(self.partial_steps)
		self.partial_steps %= 1

		schedule = sched.scheduler(time.time, time.sleep)
		for num in range(true_delta_steps):
			schedule.enter(num*time_per_tick*MILLISECOND, 1, self.ticker, ())
		schedule.run()

	# def degrees_to_delta(self, degree_table):
	# 	delta_degree_table = []
	# 	for num in range(1, len(degree_table)):
	# 		delta_degree_table.append(
	# 			degree_table[num]-degree_table[num-1]
	# 		)
	# 	return delta_degree_table

	# def schedule_movement(self, degree_table, time_interval):
	# 	delta_degree_table = self.degrees_to_delta(degree_table)

	# 	self.schedule = sched.scheduler(time.time, time.sleep)

	# 	for data_point in delta_degree_table:
	# 		arc_proportion = data_point / float(TOTAL_DEGREES)
	# 		delta_steps = (arc_proportion * MOTOR_STEPS) * self.motor_ratio	
	# 		self.partial_steps += (delta_steps % 1) #get overflow of delta
	# 		true_delta_steps = int(delta_steps) + int(self.partial_steps)
	# 		self.partial_steps %= 1

	# 		schedule.enter(time_interval, 1, self.ticker(), None)

	# def run_movement(self):
	# 	self.schedule.run()
