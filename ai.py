import math
import pygame

class Bot:

	def __init__(self, player, track):
		self.player = player
		self.track = track
		self.number_of_waypoints = len(track.waypoint_positions)
		self.current_waypoint = 1
		self.player.states[0] = True

	def think(self):
		if pygame.Rect(self.player.car.pos, self.player.car.dimensions).collidepoint(
			self.track.waypoint_positions[self.current_waypoint][0], 
			self.track.waypoint_positions[self.current_waypoint][1]
		):
			if self.current_waypoint == self.number_of_waypoints:
				self.current_waypoint = 0
			self.current_waypoint += 1
		self.dx = self.track.waypoint_positions[self.current_waypoint][0] - self.player.car.pos[0]
		self.dy = self.track.waypoint_positions[self.current_waypoint][1] - self.player.car.pos[1]
		self.ratio = math.atan2(self.dy, self.dx)
		self.angle = -self.ratio * (180/math.pi)
		self.player.car.angle = self.angle
		self.player.car.rotate()
		self.player.move()    
		
