import pygame
from tracks import test
from actor import Actor
from cfg import options

class Track:

	ACTOR_LIMIT = 16

	START = 0
	DIRT = 1
	ROAD = 2

	DIRT_COLOR = (51, 25, 0, 255)
	ROAD_COLOR = (96, 96, 96, 255)

	def __init__(self):
		self.track_data = test.track_data
		self.track_actors = []
		self.actor_dimensions = [
			options["RESOLUTION"][0] / 16,
			options["RESOLUTION"][1] / 16
		]
		for column in self.track_data:
			actor_row = []
			for row in column:
				s = pygame.Surface(self.actor_dimensions, pygame.SRCALPHA, 32)
				r = pygame.Rect(0, 0, self.actor_dimensions[0], self.actor_dimensions[1])
				if row == Track.START:
					pass
				elif row == Track.DIRT:
					pygame.draw.rect(s, Track.DIRT_COLOR, r, 0)
					actor_row.append([
						s,
						r
					])
				elif row == Track.ROAD:
					pygame.draw.rect(s, Track.ROAD_COLOR, r, 0)
					actor_row.append([
						s,
						r
					])
			self.track_actors.append(actor_row)
	
	def draw(self, surface):
		for x in range(Track.ACTOR_LIMIT):
			for y in range(Track.ACTOR_LIMIT):
				surface.blit(
					self.track_actors[y][x][0], 
					[x*int(self.actor_dimensions[0]), y*int(self.actor_dimensions[1])]
				)
			