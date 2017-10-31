import math
import pygame
from cfg import options

class Bot:

	def __init__(self, player, track):
		self.player = player
		self.track = track
		self.current_waypoint = 1
		self.previous_waypoint = 1
		self.player.states[0] = True
		self.track.choose_waypoint_path()
		self.number_of_waypoints = len(self.track.waypoint_positions.keys())
		self.future_angles = []
		for n in range(1, self.number_of_waypoints+1):
			self.dx = self.track.waypoint_positions[n][0] - self.player.car.pos[0]
			self.dy = self.track.waypoint_positions[n][1] - self.player.car.pos[1]
			self.ratio = math.atan2(self.dy, self.dx)
			self.future_angles.append(-self.ratio * (180/math.pi))
		self.get_current_waypoint_angle()

	def get_current_waypoint_angle(self):
		self.dx = self.track.waypoint_positions[self.current_waypoint][0] - self.player.car.pos[0]
		self.dy = self.track.waypoint_positions[self.current_waypoint][1] - self.player.car.pos[1]
		self.ratio = math.atan2(self.dy, self.dx)
		self.current_angle = -self.ratio * (180/math.pi)

	def think(self):
		self.previous_waypoint = self.current_waypoint
		if pygame.Rect(
				self.player.car.pos, 
				(self.player.car.dimensions[0], self.player.car.dimensions[1])).colliderect(
				pygame.Rect((
					self.track.waypoint_positions[self.current_waypoint][0], 
					self.track.waypoint_positions[self.current_waypoint][1]),
					(self.track.TRACK_SIZE, self.track.TRACK_SIZE)
				)
			):
			self.track.choose_waypoint_path()
			self.number_of_waypoints = len(self.track.waypoint_positions.keys())
			if self.current_waypoint == self.number_of_waypoints:
				self.current_waypoint = 0
			self.current_waypoint += 1
		self.get_current_waypoint_angle()
		self.player.car.angle = self.current_angle
		self.player.car.rotate()
		self.player.move()   
		
