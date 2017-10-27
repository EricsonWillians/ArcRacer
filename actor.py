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

	def __init__(self, color, pos, image_path):
		self.dimensions = [
			Car.WIDTH,
			Car.HEIGHT
		]
		Actor.__init__(self, pos, self.dimensions, image_path)
		self.rect = pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1])
		self.set_color(color)
		self.speed = 0
		self.max_speed = 4
		self.acceleration_rate = 0.1
		self.angle = 0
	
	def set_color(self, c):
		self.color = c

	def rotate(self):
		self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
		self.rect = self.rotated_surface.get_rect(center=self.surface.get_rect().center)

	def draw(self, surface):
		# pygame.draw.rect(self.surface, self.color, self.rect, 0)
		surface.blit(self.rotated_surface, self.pos)

class Player:

	def __init__(self, car):
		self.set_car(car)
		self.states = [False for x in range(4)]

	def set_car(self, car):
		self.car = car

	def move(self):
		dx = math.cos(math.radians(self.car.angle))
		dy = math.sin(math.radians(self.car.angle))
		self.car.pos = [
			self.car.pos[0] + dx * self.car.speed,
			self.car.pos[1] - dy * self.car.speed,
		]
		if self.states[0]:
			if self.car.speed < self.car.max_speed:
				self.car.speed += self.car.acceleration_rate
		else:
			if self.car.speed > 0:
				self.car.speed -= self.car.acceleration_rate
		if self.states[1]:
			if self.car.speed > -self.car.max_speed:
				self.car.speed -= self.car.acceleration_rate / 2
		else:
			if self.car.speed < 0:
				self.car.speed += self.car.acceleration_rate
		if self.states[2]:
			self.car.angle += 6
			self.car.rotate()
		if self.states[3]:
			self.car.angle -= 6
			self.car.rotate()