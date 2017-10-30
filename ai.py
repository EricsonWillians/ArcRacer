import math
import pygame

class Bot:

	def __init__(self, player, track):
		self.player = player
		self.track = track
		self.current_waypoint = 1
		self.player.states[0] = True
		self.track.choose_waypoint_path()
		self.number_of_waypoints = len(self.track.waypoint_positions.keys())
		self.get_waypoint_angle()

	def get_waypoint_angle(self):
		self.dx = self.track.waypoint_positions[self.current_waypoint][0] - self.player.car.pos[0]
		self.dy = self.track.waypoint_positions[self.current_waypoint][1] - self.player.car.pos[1]
		self.ratio = math.atan2(self.dy, self.dx)
		self.angle = -self.ratio * (180/math.pi)

	def think(self):
		if pygame.Rect(self.player.car.pos, self.player.car.dimensions).collidepoint(
			self.track.waypoint_positions[self.current_waypoint][0], 
			self.track.waypoint_positions[self.current_waypoint][1]
		):
			self.track.choose_waypoint_path()
			self.number_of_waypoints = len(self.track.waypoint_positions.keys())
			if self.current_waypoint == self.number_of_waypoints:
				self.current_waypoint = 0
			self.current_waypoint += 1
		self.get_waypoint_angle()
		if self.angle > self.player.car.angle:
			self.player.car.angle += self.player.car.steering_speed
		else:
			self.player.car.angle -= self.player.car.steering_speed
		print(self.angle, self.player.car.angle, self.player.car.gear)
		self.player.car.rotate()
		self.player.move()   
		
