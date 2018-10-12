import pygame
from actor import Actor, Car
import json
with open("cfg.json") as f:
	options = json.load(f)
from random import randint

class Track:

	SIZE = 16

	# Ground Data

	NEBULOSA = 1
	ARCPATH = 2
	NEBULOSA_IMAGE = "gfx/nebulosa.png"
	ARCPATH_IMAGE = "gfx/arcpath.png"

	# Actors

	ARCFINISH_BACK = 1	
	ARCFINISH = 2	
	ARCFINISH_FRONT = 3
	ARCFINISH_IMAGE = "gfx/arcfinish.png"
	ARCFINISH_BACK_IMAGE = "gfx/arcfinish_back.png"
	ARCFINISH_FRONT_IMAGE = "gfx/arcfinish_front.png"

	def __init__(self, loaded_track):
		self.track = loaded_track
		self.name = self.track["name"]
		self.ground_data = self.track["ground_data"]	
		self.waypoints = self.track["waypoints"]
		self.spawnpoints = self.track["spawnpoints"]	
		self.actorpoints = self.track["actorpoints"]
		self.ground_positions = {}
		self.waypoint_positions = {}
		self.spawn_positions = {}
		self.ground_tiles = []
		self.actors = []
		self.actor_positions = {}
		self.current_waypoint_path = 0
		self.ground_tile_dimensions = [
			int(options["RESOLUTION"][0] / 16),
			int(options["RESOLUTION"][1] / 16)
		]
		self.actor_dimensions = [
			int(options["RESOLUTION"][0] / 16),
			int(options["RESOLUTION"][1] / 16)
		]
		self.surface = pygame.Surface((options["RESOLUTION"][0], options["RESOLUTION"][1]), pygame.SRCALPHA, 32)
		
		# Iterating over the track's ground data		
		
		for row in self.ground_data:
			ground_tile_row = []
			for column in row:
				if column == Track.NEBULOSA:
					img = pygame.transform.scale(
						pygame.image.load(Track.NEBULOSA_IMAGE), 
						self.ground_tile_dimensions
					)
					ground_tile_row.append(img)
				elif column == Track.ARCPATH:
					img = pygame.transform.scale(
						pygame.image.load(Track.ARCPATH_IMAGE), 
						self.ground_tile_dimensions
					)
					ground_tile_row.append(img)
			self.ground_tiles.append(ground_tile_row)
		
		# Iterating over the track's actor data		

		for row in self.actorpoints:
			actor_row = []
			for column in row:
				if column == Track.ARCFINISH:
					img = pygame.transform.scale(
						pygame.image.load(Track.ARCFINISH_IMAGE), 
						self.actor_dimensions
					)
					actor_row.append(img)
				elif column == Track.ARCFINISH_BACK:
					img = pygame.transform.scale(
						pygame.image.load(Track.ARCFINISH_BACK_IMAGE), 
						self.actor_dimensions
					)
					actor_row.append(img)
				elif column == Track.ARCFINISH_FRONT:
					img = pygame.transform.scale(
						pygame.image.load(Track.ARCFINISH_FRONT_IMAGE), 
						self.actor_dimensions
					)
					actor_row.append(img)
				else:
					actor_row.append(None)
			self.actors.append(actor_row)

		for y in range(Track.SIZE):
			for x in range(Track.SIZE):
				# Important to notice:
				# ground_positions and actor_positions have positions as keys,
				# as opposed to spawn_positions, as they use repeated numbers.
				# Waypoints are sequencial, so the positions can be stored using them as key.
				# Tiles are repeated, so if their positions were stored by their respective numbers,
				# the positions would be overwritten within the loop.
				if self.ground_data[y][x] != 0:
					self.ground_positions[(
						x*int(self.ground_tile_dimensions[0]),
						y*int(self.ground_tile_dimensions[1])
					)] = self.ground_data[y][x]
				if self.actorpoints[y][x] != 0:
					self.actor_positions[(
						x*int(self.actor_dimensions[0]) + Car.WIDTH,
						y*int(self.actor_dimensions[1]) + Car.HEIGHT
					)] = self.actorpoints[y][x]
				if self.spawnpoints[y][x] != 0:
					self.spawn_positions[self.spawnpoints[y][x]] = (
						x*int(self.ground_tile_dimensions[0]) + Car.WIDTH,
						y*int(self.ground_tile_dimensions[1]) + Car.HEIGHT
					)
		# Blitting the track images to the track surface for greater performance.
		for y in range(Track.SIZE):
			for x in range(Track.SIZE):
				self.surface.blit(
					self.ground_tiles[y][x], 
					[x*int(self.ground_tile_dimensions[0]), y*int(self.ground_tile_dimensions[1])]
				)
		# Blitting static actors.
		for y in range(Track.SIZE):
			for x in range(Track.SIZE):
				if self.actors[y][x]:
					self.surface.blit(
						self.actors[y][x], 
						[x*int(self.actor_dimensions[0]), y*int(self.actor_dimensions[1])]
					)

	def choose_waypoint_path(self):
		self.current_waypoint_path = randint(0, len(self.waypoints)-1)
		for y in range(Track.SIZE):
			for x in range(Track.SIZE):
				if self.waypoints[self.current_waypoint_path][y][x] != 0:
					self.waypoint_positions[self.waypoints[self.current_waypoint_path][y][x]] = (
						x*int(self.ground_tile_dimensions[0]) + Car.WIDTH,
						y*int(self.ground_tile_dimensions[1]) + Car.HEIGHT
					)

	def draw(self, surface):
		surface.blit(self.surface, (0, 0))
			
