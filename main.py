import sys
import pygame
from PyGameWidgets import core, widgets
from cfg import options
import actor
import ui
import track
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir)

from tracks import tracks

print("Initializing game with the following options: \n{opt}".format(opt=options))

class SceneManager:

	MAIN_MENU = 0
	RACE_OPTIONS = 1
	GAME = 2
	PAUSE = 3

	def __init__(self):
		self.scene = 0

	def change_scene(self, scene):
		self.scene = scene

if __name__ == "__main__":

	# Pygame

	WINDOW_WIDTH = options["RESOLUTION"][0]
	WINDOW_HEIGHT = options["RESOLUTION"][1]
	pygame.init()
	pygame.font.init
	if options["FULLSCREEN"]:
		screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	clock = pygame.time.Clock()
	FPS = 60
	running = True

	# Game-specific

	loaded_tracks = [t for t in tracks]
	test_track = track.Track(loaded_tracks[0])
	players = [
		actor.Player(actor.Car(test_track.spawn_positions[n], "gfx/player{_n}.png".format(_n=n))) for n in range(1, 6)
	]

	sm = SceneManager()
	number_of_humans = 2
	number_of_players = 5
	max_player_slot = 5

	main_menu = ui.MainMenu()
	race_options = ui.RaceOptions()
	pause_screen = ui.PauseScreen()

	def redraw():
		pygame.display.flip()
		screen.fill(core.BLACK)
		if sm.scene == SceneManager.MAIN_MENU:
			main_menu.draw(screen)
		elif sm.scene == SceneManager.RACE_OPTIONS:
			race_options.draw(screen)
		elif sm.scene == SceneManager.GAME:
			test_track.draw(screen)
			[p.car.draw(screen) for p in players]
		elif sm.scene == SceneManager.PAUSE:
			pause_screen.draw(screen)

	def intercept_in_game(e):
		for n in range(number_of_humans):
			if e.type == pygame.KEYDOWN:
				# Movement-related
				if e.key == options["PLAYER{_n}_ACCELERATE".format(_n=n+1)]:
					players[n].states[0] = True
				elif e.key == options["PLAYER{_n}_REVERSE".format(_n=n+1)]:
					players[n].states[1] = True
				elif e.key == options["PLAYER{_n}_STEER_LEFT".format(_n=n+1)]:
					players[n].states[2] = True	
				elif e.key == options["PLAYER{_n}_STEER_RIGHT".format(_n=n+1)]:
					players[n].states[3] = True
				# Other
				elif e.key == options["PAUSE"]:
					sm.change_scene(SceneManager.PAUSE)
				elif e.key == pygame.K_ESCAPE:
					sm.change_scene(SceneManager.MAIN_MENU)
			elif e.type == pygame.KEYUP:	
				if e.key == options["PLAYER{_n}_ACCELERATE".format(_n=n+1)]:
					players[n].states[0] = False
				elif e.key == options["PLAYER{_n}_REVERSE".format(_n=n+1)]:
					players[n].states[1] = False
				elif e.key == options["PLAYER{_n}_STEER_LEFT".format(_n=n+1)]:
					players[n].states[2] = False
				elif e.key == options["PLAYER{_n}_STEER_RIGHT".format(_n=n+1)]:
					players[n].states[3] = False
		for n in range(number_of_humans, max_player_slot):
			pass

	def intercept_in_race_options(e):
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				sm.change_scene(SceneManager.MAIN_MENU)

	def intercept_in_pause(e):
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				sm.change_scene(SceneManager.GAME)

	while (running):
		clock.tick(FPS)
		redraw()
		if sm.scene == SceneManager.GAME:
			for n in range(number_of_humans):
				players[n].move(test_track)
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				sys.exit()
			if sm.scene == SceneManager.MAIN_MENU:
				main_menu.buttons[0].on_click(e, sm.change_scene, SceneManager.RACE_OPTIONS)
				main_menu.buttons[1].on_click(e, lambda: sys.exit())
			elif sm.scene == SceneManager.RACE_OPTIONS:
				intercept_in_race_options(e)
				for c in race_options.components:
					if isinstance(c, widgets.OptionChooser):
						c.activate(e)
				race_options.components[0].on_click(e, sm.change_scene, SceneManager.GAME)
				race_options.components[3].on_click(e, sm.change_scene, SceneManager.MAIN_MENU)
			elif sm.scene == SceneManager.GAME:
				intercept_in_game(e)
			elif sm.scene == SceneManager.PAUSE:
				intercept_in_pause(e)
		