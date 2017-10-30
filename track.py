import pygame
from actor import Actor, Car
from cfg import options

class Track:

	TRACK_SIZE = 16

	DIRT = 1
	ROAD = 2

	DIRT_IMAGE = "gfx/dirt.png"
	ROAD_IMAGE = "gfx/road.png"

	def __init__(self, track):
		self.track = track
		self.ground_data = self.track.ground_data
		self.spawnpoints = self.track.spawnpoints
		self.waypoints = self.track.waypoints
		self.actors = []
		self.ground_positions = {}
		self.spawn_positions = {}
		self.waypoint_positions = {}
		self.actor_dimensions = [
			int(options["RESOLUTION"][0] / 16),
			int(options["RESOLUTION"][1] / 16)
		]
		self.surface = pygame.Surface((options["RESOLUTION"][0], options["RESOLUTION"][1]), pygame.SRCALPHA, 32)
		for row in self.ground_data:
			actor_row = []
			for column in row:
				if column == Track.DIRT:
					img = pygame.transform.scale(
						pygame.image.load(Track.DIRT_IMAGE), 
						self.actor_dimensions
					)
					actor_row.append(img)
				elif column == Track.ROAD:
					img = pygame.transform.scale(
						pygame.image.load(Track.ROAD_IMAGE), 
						self.actor_dimensions
					)
					actor_row.append(img)
			self.actors.append(actor_row)
		for y in range(Track.TRACK_SIZE):
			for x in range(Track.TRACK_SIZE):
				if self.ground_data[y][x] != 0:
					self.ground_positions[(
						x*int(self.actor_dimensions[0]),
						y*int(self.actor_dimensions[1])
					)] = self.ground_data[y][x]
				if self.spawnpoints[y][x] != 0:
					self.spawn_positions[self.spawnpoints[y][x]] = (
						x*int(self.actor_dimensions[0]) + Car.WIDTH,
						y*int(self.actor_dimensions[1]) + Car.HEIGHT
					)
				if self.waypoints[y][x] != 0:
					self.waypoint_positions[self.waypoints[y][x]] = (
						x*int(self.actor_dimensions[0]) + Car.WIDTH,
						y*int(self.actor_dimensions[1]) + Car.HEIGHT
					)
		# Blitting the track images to the track surface for greater performance.
		for y in range(Track.TRACK_SIZE):
			for x in range(Track.TRACK_SIZE):
				self.surface.blit(
					self.actors[y][x], 
					[x*int(self.actor_dimensions[0]), y*int(self.actor_dimensions[1])]
				)

	def draw(self, surface):
		surface.blit(self.surface, (0, 0))
			