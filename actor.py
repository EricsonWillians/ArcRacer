import pygame
import math
import json
import util

with open("cfg.json") as f:
	options = json.load(f)

class Actor:
	
	def __init__(self, pos, dimensions, image_path):
		self.surface = pygame.Surface(dimensions, pygame.SRCALPHA, 32)
		self.set_pos(pos)
		self.set_image(image_path)
		self.rotated_surface = self.surface

	def set_pos(self, pos):
		self.pos = pos

	def set_image(self, path):
		self.image = pygame.image.load(path)
		self.surface.blit(self.image, (0, 0))

class Car(Actor):
	
	WIDTH = 24
	HEIGHT = 18
	NEBULOSA_DEACCELERATION_RATE = 0.2
	NEBULOSA_MININUM_SPEED = 1.5
	REAR_ACCELERATION_RATE = 0.010
	MAXIMUM_GEARS = 6
	OFF_SCREEN_BOUNCING_ACCELERATION = 100

	def __init__(self, pos, image_path):
		self.dimensions = [
			Car.WIDTH,
			Car.HEIGHT
		]
		Actor.__init__(self, pos, self.dimensions, image_path)
		self.speed = 0
		self.steering_speed = 1.8
		self.max_speed = 6
		self.rear_max_speed = 1.5
		self.acceleration_rate = 0.0
		self.gear = 0
		self.gear_changing_delay = 45
		self.angle = 0
	
	def rotate(self):
		self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)

	def draw(self, surface):
		surface.blit(self.rotated_surface, self.pos)

class Player:

	def __init__(self, car, track, name):
		self.set_car(car)
		self.states = [False for x in range(4)]
		self.track = track
		self.name = name
		self.position = 1
		self.raw_time_in_milliseconds = 0
		self.time = {}
		self.reached_lap = False
		self.crossed_lap = False
		self.current_lap = 1
		self.laps = {}
		self.lap_timestamps = {
			1: ("--", "--", "--")
		}
		for n in range(99):
			self.laps[n] = 0
		self.clock = 0

	def get_time_to_clear_laps(self):
		time = 0
		for lap in self.laps:
			time += self.laps[lap]
		return time 

	def set_car(self, car):
		self.car = car

	def track_time(self, ms):
		self.raw_time_in_milliseconds += ms
		converted = util.convert_ms(self.raw_time_in_milliseconds)
		self.time["milliseconds"] = converted[0]
		self.time["seconds"] = int(converted[1])
		self.time["minutes"] = int(converted[2])
		self.time["hours"] = int(converted[3])

	def move(self, handicap=0):
		dx = math.cos(math.radians(self.car.angle))
		dy = math.sin(math.radians(self.car.angle))
		self.car.pos = [
			self.car.pos[0] + dx * self.car.speed,
			self.car.pos[1] - dy * self.car.speed,
		]
		if self.car.gear == 0:
			self.car.acceleration_rate = 0
		elif self.car.gear == 1:
			self.car.acceleration_rate = 0.05
		elif self.car.gear == 2:
			self.car.acceleration_rate = 0.010
		elif self.car.gear == 3:
			self.car.acceleration_rate = 0.025
		elif self.car.gear == 4:
			self.car.acceleration_rate = 0.050
		elif self.car.gear == 5:
			self.car.acceleration_rate = 0.075
		elif self.car.gear == 6:
			self.car.acceleration_rate = 0.1
		def deaccelerate(_dir, _min, accel):
			def reduce_gear():
				if self.clock == self.car.gear_changing_delay: 
					if self.car.gear > 0:
						self.car.gear -= 1
					self.clock = 0
				self.clock += 1
			if _dir: # 0 = UP, 1 = DOWN
				if self.car.speed > _min:
					self.car.speed -= accel
					reduce_gear()
			else:
				if self.car.speed < _min:
					self.car.speed += accel
					reduce_gear()
		# Up
		if self.states[0]:
			if self.car.speed < self.car.max_speed:
				self.car.speed += self.car.acceleration_rate + handicap
				if self.clock == self.car.gear_changing_delay: 
					if self.car.gear <= Car.MAXIMUM_GEARS:
						self.car.gear += 1
					self.clock = 0
				self.clock += 1
		else:
			# When you release the up key, 
			# the car deaccelerates / comes to a minimal value.
			deaccelerate(1, 0, self.car.acceleration_rate)
		# Down
		if self.states[1]:
			if self.car.speed > -self.car.rear_max_speed:
				self.car.speed -= Car.REAR_ACCELERATION_RATE
		else:
			deaccelerate(0, 0, self.car.acceleration_rate)
		# Left
		if self.states[2]:
			self.car.angle += self.car.steering_speed
			self.car.rotate()
		# Right
		if self.states[3]:
			self.car.angle -= self.car.steering_speed
			self.car.rotate()

		# Handling off-screen presence
		if (self.car.pos[0] - self.car.dimensions[0]) > options["RESOLUTION"][0] or (self.car.pos[1] - self.car.dimensions[1]) > options["RESOLUTION"][1] or self.car.pos[0] < 0 or self.car.pos[1] < 0:
			self.car.speed -= (self.car.acceleration_rate + handicap) * Car.OFF_SCREEN_BOUNCING_ACCELERATION

		# Handling ground collision
		for pos in self.track.ground_positions.keys():
			if pygame.Rect(pos, (self.track.ground_tile_dimensions[0], self.track.ground_tile_dimensions[1])).colliderect(pygame.Rect(self.car.pos, self.car.dimensions)):
				# Movement interference
				if self.track.ground_positions[pos] == self.track.NEBULOSA:
					if self.states[0]:
						deaccelerate(1, Car.NEBULOSA_MININUM_SPEED, Car.NEBULOSA_DEACCELERATION_RATE)
					if self.states[1]:
						deaccelerate(0, -Car.NEBULOSA_MININUM_SPEED, Car.NEBULOSA_DEACCELERATION_RATE)

		# Handling actor collision
		for pos in self.track.actor_positions.keys():
			if pygame.Rect(pos, (self.track.actor_dimensions[0], self.track.actor_dimensions[1])).colliderect(pygame.Rect(self.car.pos, self.car.dimensions)):
				# Handling lap logic
				if self.track.actor_positions[pos] == self.track.ARCFINISH_BACK:
					if self.crossed_lap:
						self.reached_lap = True
						self.crossed_lap = False
				elif self.track.actor_positions[pos] == self.track.ARCFINISH:
					if self.reached_lap:
						self.current_lap += 1
						self.lap_timestamps[self.current_lap] = (self.time["minutes"], self.time["seconds"], self.time["milliseconds"])
						self.reached_lap = False
				elif self.track.actor_positions[pos] == self.track.ARCFINISH_FRONT:
					self.crossed_lap = True
					self.laps[self.current_lap] += 1
						
