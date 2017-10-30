import math

class Bot:

	def __init__(self, player, track):
		self.player = player
		self.track = track
		self.number_of_waypoints = len(track.waypoint_positions)
		self.current_waypoint = 2
		self.dx = self.track.waypoint_positions[self.current_waypoint][0] - self.player.car.pos[0]
		self.dy = self.track.waypoint_positions[self.current_waypoint][1] - self.player.car.pos[1]
		self.angle = math.atan2(self.dy, self.dx)
		self.player.car.angle = self.angle
		self.player.states[0] = True

	def think(self):
		
		self.player.car.rotate()
		self.player.move()    