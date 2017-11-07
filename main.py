import sys
import pygame
from PyGameWidgets import core, widgets
from cfg import options
import actor
import ui
import hud
import ai
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

class GameManager:

	def __init__(self, loaded_tracks):
		self.loaded_tracks = loaded_tracks
		self.current_track = self.loaded_tracks[0]
		self.default()

	def get_track_list(self):
		path = "tracks"
		tracks = [f[:-3] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
		tracks.remove("__init__")
		return tracks

	def update_racing_positions(self):
		for p in self.players:
			self.checkpoints_cleared_of_all_players[p.name] = p.checkpoints_cleared
		self.racing_positions = sorted(
			self.checkpoints_cleared_of_all_players.keys(), 
			key=lambda k: self.checkpoints_cleared_of_all_players[k], 
			reverse=True
		)

	def get_player_racing_position_by_name(self, name):
		for p in self.players:
			if p.name == name:
				return self.racing_positions.index(name)+1 # We can't have a 0 racing position.

	def set_number_of_players(self, n):
		self.number_of_players = n
		self.players = [
			actor.Player(
				actor.Car(
					self.current_track.spawn_positions[n], 
					"gfx/player{_n}.png".format(_n=n)
				), 
				self.current_track,
				'P'+str(n)
			) for n in range(1, self.number_of_players+1)
		]
		if self.number_of_humans == 1:
			self.bots = [
				ai.Bot(p, self.current_track) for p in self.players if p != self.players[0]
			]
		elif self.number_of_humans == 2:
			self.bots = [
				ai.Bot(p, self.current_track) for p in self.players if p != self.players[0] and p != self.players[1]
			]

	def set_number_of_humans(self, n):
		self.number_of_humans = n
		if self.number_of_humans == 2 and self.number_of_players == 1:
			self.set_number_of_players(2)

	def set_difficulty(self, d):
		if d == "Easy":
			self.difficulty = 0.50
		elif d == "Normal":
			self.difficulty = 1.75
		elif d == "Hard":
			self.difficulty = 3.50
		elif d == "Insane":
			self.difficulty = 3.75
		elif d == "Arcturian":
			self.difficulty = 4.00

	def set_laps(self, l):
		self.laps = int(l)

	def set_track(self, track_name):
		for t in self.loaded_tracks:
			if t.name == track_name:
				self.current_track = t

	def default(self):
		self.number_of_humans = 1
		self.number_of_players = 1
		self.max_player_slot = 5
		self.set_number_of_players(self.number_of_players)
		self.checkpoints_cleared_of_all_players = {}
		self.racing_positions = []
		self.update_racing_positions()
		self.set_difficulty("Normal")
		self.set_laps(15)

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

	loaded_tracks = [track.Track(t) for t in tracks]
	
	sm = SceneManager()
	gm = GameManager(loaded_tracks)
	main_menu = ui.MainMenu()
	race_options = ui.RaceOptions(gm)
	game_hud = hud.HUD(gm)
	pause_screen = ui.PauseScreen()

	def redraw():
		pygame.display.flip()
		screen.fill(core.BLACK)
		if sm.scene == SceneManager.MAIN_MENU:
			main_menu.draw(screen)
		elif sm.scene == SceneManager.RACE_OPTIONS:
			race_options.draw(screen)
		elif sm.scene == SceneManager.GAME:
			gm.current_track.draw(screen)
			[p.car.draw(screen) for p in gm.players]
			game_hud.draw(screen)
		elif sm.scene == SceneManager.PAUSE:
			pause_screen.draw(screen)

	def intercept_in_game(e):
		for n in range(gm.number_of_humans):
			if e.type == pygame.KEYDOWN:
				# Movement-related
				if e.key == options["PLAYER{_n}_ACCELERATE".format(_n=n+1)]:
					gm.players[n].states[0] = True
				elif e.key == options["PLAYER{_n}_REVERSE".format(_n=n+1)]:
					gm.players[n].states[1] = True
				elif e.key == options["PLAYER{_n}_STEER_LEFT".format(_n=n+1)]:
					gm.players[n].states[2] = True	
				elif e.key == options["PLAYER{_n}_STEER_RIGHT".format(_n=n+1)]:
					gm.players[n].states[3] = True
				# Other
				elif e.key == options["PAUSE"]:
					sm.change_scene(SceneManager.PAUSE)
				elif e.key == pygame.K_ESCAPE:
					gm.default()
					sm.change_scene(SceneManager.MAIN_MENU)
			elif e.type == pygame.KEYUP:	
				if e.key == options["PLAYER{_n}_ACCELERATE".format(_n=n+1)]:
					gm.players[n].states[0] = False
				elif e.key == options["PLAYER{_n}_REVERSE".format(_n=n+1)]:
					gm.players[n].states[1] = False
				elif e.key == options["PLAYER{_n}_STEER_LEFT".format(_n=n+1)]:
					gm.players[n].states[2] = False
				elif e.key == options["PLAYER{_n}_STEER_RIGHT".format(_n=n+1)]:
					gm.players[n].states[3] = False
		for n in range(gm.number_of_humans, gm.max_player_slot):
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
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				sys.exit()
			if sm.scene == SceneManager.MAIN_MENU:
				main_menu.buttons[2].on_click(e, sm.change_scene, SceneManager.RACE_OPTIONS)
				main_menu.buttons[3].on_click(e, lambda: sys.exit())
			elif sm.scene == SceneManager.RACE_OPTIONS:
				intercept_in_race_options(e)
				for c in race_options.components:
					if isinstance(c, widgets.OptionChooser):
						c.activate(e)
				race_options.components[0].on_click(e, sm.change_scene, SceneManager.GAME)
				race_options.components[2].on_change(e, 
					gm.set_number_of_players,
					int(race_options.components[2].current_value)
				)
				race_options.components[4].on_change(e, 
					gm.set_number_of_humans,
					int(race_options.components[4].current_value)
				)
				race_options.components[6].on_change(e, 
					gm.set_difficulty,
					race_options.components[6].current_value
				)
				race_options.components[8].on_change(e, 
					gm.set_laps,
					int(race_options.components[8].current_value)
				)
				race_options.components[10].on_change(e, 
					gm.set_track,
					race_options.components[10].current_value
				)
				race_options.components[11].on_click(e, sm.change_scene, SceneManager.MAIN_MENU)
			elif sm.scene == SceneManager.GAME:
				intercept_in_game(e)
			elif sm.scene == SceneManager.PAUSE:
				intercept_in_pause(e)
		if sm.scene == SceneManager.RACE_OPTIONS:
			race_options.components[2].current_value = str(gm.number_of_players)
			race_options.components[2].text = core.Text(gm.number_of_players, ui.RACE_OPTIONS_MENU_SIZE, ui.RACE_OPTIONS_MENU_COLOR, ui.RACE_OPTIONS_MENU_FONT, ui.RACE_OPTIONS_MENU_BOLD, ui.RACE_OPTIONS_MENU_ITALIC)
			race_options.components[2].update_text()
		elif sm.scene == SceneManager.GAME:
			for n in range(gm.number_of_humans):
				gm.players[n].move()
			for bot in gm.bots:
				bot.think(gm.difficulty)	
			gm.update_racing_positions()
			# Updating the text of the player info panels.
			game_hud.player1_info_panel_labels[2].set_text(
				core.Text("{0:.2f}".format(round(gm.players[0].car.speed, 2)), game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
			)
			game_hud.player1_info_panel_labels[4].set_text(
				core.Text(str(gm.players[0].car.gear), game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
			)
			game_hud.player1_info_panel_labels[6].set_text(
				core.Text(str(gm.get_player_racing_position_by_name("P1")), game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
			)
			game_hud.player1_info_panel_labels[8].set_text(
				core.Text(str(gm.players[0].current_lap), game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
			)
			if gm.number_of_humans == 2:
				game_hud.player2_info_panel_labels[2].set_text(
					core.Text("{0:.2f}".format(round(gm.players[1].car.speed, 2)), game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
				)
				game_hud.player2_info_panel_labels[4].set_text(
					core.Text(str(gm.players[1].car.gear), game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
				)
				game_hud.player2_info_panel_labels[6].set_text(
					core.Text(str(gm.get_player_racing_position_by_name("P2")), game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
				)
				game_hud.player2_info_panel_labels[8].set_text(
					core.Text(str(gm.players[1].current_lap), game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
				)
				

			