import pygame
from tracks import test
from actor import Actor, Car
from cfg import options

class Track:

	TRACK_SIZE = 16

	START = 0
	DIRT = 1
	ROAD = 2

	DIRT_IMAGE = "gfx/dirt.png"
	ROAD_IMAGE = "gfx/road.png"

	def __init__(self):
		self.data = test.track_data
		self.spawnpoints = test.track_spawnpoints
		self.waypoints = test.track_waypoints
		self.actors = []
		self.spawn_positions = {}
		self.actor_dimensions = [
			options["RESOLUTION"][0] / 16,
			options["RESOLUTION"][1] / 16
		]
		self.surface = pygame.Surface((options["RESOLUTION"][0], options["RESOLUTION"][1]), pygame.SRCALPHA, 32)
		for row in self.data:
			actor_row = []
			for column in row:
				if column == Track.START:
					pass
				elif column == Track.DIRT:
					actor_row.append(pygame.image.load(Track.DIRT_IMAGE))
				elif column == Track.ROAD:
					actor_row.append(pygame.image.load(Track.ROAD_IMAGE))
			self.actors.append(actor_row)
		occurence_counter = 0
		for y in range(Track.TRACK_SIZE):
			for x in range(Track.TRACK_SIZE):
				if self.spawnpoints[y][x] != 0:
					self.spawn_positions[occurence_counter] = (
						x*int(self.actor_dimensions[0]) + Car.WIDTH,
						y*int(self.actor_dimensions[1]) + Car.HEIGHT
					)
					occurence_counter += 1
		# Blitting the track images to the track surface for greater performance.
		for y in range(Track.TRACK_SIZE):
			for x in range(Track.TRACK_SIZE):
				self.surface.blit(
					self.actors[y][x], 
					[x*int(self.actor_dimensions[0]), y*int(self.actor_dimensions[1])]
				)

	def draw(self, surface):
		surface.blit(self.surface, (0, 0))
			