import pygame
import math

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
	DIRT_DEACCELERATION_RATE = 0.2
	DIRT_MININUM_SPEED = 1.5

	def __init__(self, pos, image_path):
		self.dimensions = [
			Car.WIDTH,
			Car.HEIGHT
		]
		Actor.__init__(self, pos, self.dimensions, image_path)
		self.speed = 0
		self.steering_speed = 6
		self.max_speed = 4
		self.acceleration_rate = 0.1
		self.angle = 0
	
	def rotate(self):
		self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)

	def draw(self, surface):
		surface.blit(self.rotated_surface, self.pos)

class Player:

	def __init__(self, car, track):
		self.set_car(car)
		self.states = [False for x in range(4)]
		self.track = track

	def set_car(self, car):
		self.car = car

	def move(self):
		dx = math.cos(math.radians(self.car.angle))
		dy = math.sin(math.radians(self.car.angle))
		self.car.pos = [
			self.car.pos[0] + dx * self.car.speed,
			self.car.pos[1] - dy * self.car.speed,
		]
		def deaccelerate(d, _min, accel):
			if d:
				if self.car.speed > _min:
					self.car.speed -= accel
			else:
				if self.car.speed < _min:
					self.car.speed += accel
		# Up
		if self.states[0]:
			if self.car.speed < self.car.max_speed:
				self.car.speed += self.car.acceleration_rate
		else:
			# When you release the up key, 
			# the car deaccelerates / comes to a minimal value.
			deaccelerate(1, 0, self.car.acceleration_rate)
		# Down
		if self.states[1]:
			if self.car.speed > -self.car.max_speed:
				self.car.speed -= self.car.acceleration_rate / 2
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
		# Track-related
		# Here comes anything from the track that affects the movement, 
		# like different types of ground and obstacles.
		for p in self.track.ground_positions.keys():
			if pygame.Rect(p, (self.track.actor_dimensions[0], self.track.actor_dimensions[1])).collidepoint(self.car.pos[0], self.car.pos[1]):
				if self.track.ground_positions[p] == self.track.DIRT:
					if self.states[0]:
						deaccelerate(1, Car.DIRT_MININUM_SPEED, Car.DIRT_DEACCELERATION_RATE)
					if self.states[1]:
						deaccelerate(0, -Car.DIRT_MININUM_SPEED, Car.DIRT_DEACCELERATION_RATE)