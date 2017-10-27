import sys
import pygame
from PyGameWidgets import core
from cfg import options
import actor
import ui
import track

# Widget border example.

print("Initializing game with the following options: \n{opt}".format(opt=options))

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

class SceneManager:

	MAIN_MENU = 0
	GAME = 1
	PAUSE = 2

	def __init__(self):
		self.scene = 0

	def change_scene(self, scene):
		self.scene = scene

if __name__ == "__main__":
	sm = SceneManager()
	test_track = track.Track()
	players = [
		actor.Player(actor.Car(test_track.spawn_positions[1], "gfx/player1.png")),
		actor.Player(actor.Car(test_track.spawn_positions[2], "gfx/player2.png"))
	]
	main_menu = ui.MainMenu()
	pause_screen = ui.PauseScreen()
	def redraw():
		pygame.display.flip()
		screen.fill(core.BLACK)
		if sm.scene == SceneManager.MAIN_MENU:
			main_menu.draw(screen)
		elif sm.scene == SceneManager.GAME:
			test_track.draw(screen)
			[p.car.draw(screen) for p in players]
		elif sm.scene == SceneManager.PAUSE:
			pause_screen.draw(screen)

	def intercept_in_game(e):
		if e.type == pygame.KEYDOWN:
			# Movement-related
			if e.key == pygame.K_UP:
				players[0].states[0] = True
			elif e.key == pygame.K_DOWN:
				players[0].states[1] = True
			elif e.key == pygame.K_LEFT:
				players[0].states[2] = True	
			elif e.key == pygame.K_RIGHT:
				players[0].states[3] = True
			# Other
			elif e.key == pygame.K_p:
				sm.change_scene(SceneManager.PAUSE)
			elif e.key == pygame.K_ESCAPE:
				sm.change_scene(SceneManager.MAIN_MENU)
		elif e.type == pygame.KEYUP:	
			if e.key == pygame.K_UP:
				players[0].states[0] = False
			elif e.key == pygame.K_DOWN:
				players[0].states[1] = False
			elif e.key == pygame.K_LEFT:
				players[0].states[2] = False
			elif e.key == pygame.K_RIGHT:
				players[0].states[3] = False
	def intercept_in_pause(e):
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				sm.change_scene(SceneManager.GAME)

	while (running):
		clock.tick(FPS)
		redraw()
		if sm.scene == SceneManager.GAME:
			players[0].move(test_track)
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				sys.exit()
			if sm.scene == SceneManager.MAIN_MENU:
				main_menu.buttons[0].on_click(e, sm.change_scene, SceneManager.GAME)
				main_menu.buttons[1].on_click(e, lambda: sys.exit())
			elif sm.scene == SceneManager.GAME:
				intercept_in_game(e)
			elif sm.scene == SceneManager.PAUSE:
				intercept_in_pause(e)
		