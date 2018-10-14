import sys
import pygame
from PyGameWidgets import core, widgets
import json
with open("cfg.json") as f:
	options = json.load(f)
import actor
import ui
import hud
import ai
import track
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir)

class SceneManager:

	MAIN_MENU = 0
	RACE_OPTIONS = 1
	GAME = 2
	RESULTS = 3
	PAUSE = 4

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
		return [track.name for track in self.loaded_tracks]

	def get_player_racing_position_by_name(self, name):
		pass

	def set_number_of_players(self, n):
		self.bots = []
		self.number_of_players = n
		self.players = [
			actor.Player(
				actor.Car(
					self.current_track.spawn_positions[n], 
					f"gfx/player{n}.png"
				), 
				self.current_track,
				f'P{n}'
			) for n in range(1, self.number_of_players+1)
		]
		
		# If 1 player is human, all the others are bots.
		# If 2 players are humans (Local oldschool keyboard multiplayer), then the second slot is also reserved.
		# If there are no human players, then the bots play by themselves.

		if self.number_of_humans == 0:
			self.bots = [ai.Bot(p, self.current_track) for p in self.players]
		elif self.number_of_humans == 1:
			self.bots = [
				ai.Bot(p, self.current_track) for p in self.players if p != self.players[0]
			]
		elif self.number_of_humans == 2:
			self.bots = [
				ai.Bot(p, self.current_track) for p in self.players if p != self.players[0] and p != self.players[1]
			]
		
		for player in self.players:
			self.racing_positions[player.name] = 0

	def set_number_of_humans(self, n):
		self.number_of_humans = n
		if self.number_of_humans < 3:
			self.set_number_of_players(n)

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
		self.number_of_humans = 0
		self.number_of_players = 0
		self.bots = []
		self.players = []
		self.difficulty = 1.75
		self.laps = 5
		self.max_player_slot = 5
		self.racing_positions = {}

if __name__ == "__main__":

	# Pygame

	os.environ["SDL_VIDEO_CENTERED"] = '1'
	WINDOW_WIDTH = options["RESOLUTION"][0]
	WINDOW_HEIGHT = options["RESOLUTION"][1]
	pygame.init()
	pygame.font.init
	if eval(options["FULLSCREEN"]):
		screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	clock = pygame.time.Clock()
	FPS = 60
	running = True

	# Game-specific
	
	track_names = [t for t in os.listdir("tracks") if os.path.isfile(os.path.join("tracks", t)) and t.endswith(".json")]
	loaded_tracks = []	
	for track_name in track_names:
		with open(f"tracks/{track_name}") as t:	
			loaded_tracks.append(track.Track(json.load(t)))
		print(f"Loading track: {track_name}")

	sm = SceneManager()
	gm = GameManager(loaded_tracks)
	main_menu = ui.MainMenu()
	race_options = ui.RaceOptions(gm)
	results = ui.Results(gm)
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
		elif sm.scene == SceneManager.RESULTS:
			results.draw(screen)
		elif sm.scene == SceneManager.PAUSE:
			pause_screen.draw(screen)

	def intercept_in_game(e):

		if e.type == pygame.KEYDOWN:
			# Movement-related
			for n in range(gm.number_of_humans):
				if e.key == eval(options["PLAYER{_n}_ACCELERATE".format(_n=n+1)]):
					gm.players[n].states[0] = True
				elif e.key == eval(options["PLAYER{_n}_REVERSE".format(_n=n+1)]):
					gm.players[n].states[1] = True
				elif e.key == eval(options["PLAYER{_n}_STEER_LEFT".format(_n=n+1)]):
					gm.players[n].states[2] = True	
				elif e.key == eval(options["PLAYER{_n}_STEER_RIGHT".format(_n=n+1)]):
					gm.players[n].states[3] = True
			# Other
			if e.key == eval(options["PAUSE"]):
				sm.change_scene(SceneManager.PAUSE)
			elif e.key == pygame.K_ESCAPE:
				gm.default()
				sm.change_scene(SceneManager.MAIN_MENU)
			elif e.key == pygame.K_F12:
				gm.default()
				sm.change_scene(SceneManager.RESULTS)
		elif e.type == pygame.KEYUP:	
			for n in range(gm.number_of_humans):
				if e.key == eval(options["PLAYER{_n}_ACCELERATE".format(_n=n+1)]):
					gm.players[n].states[0] = False
				elif e.key == eval(options["PLAYER{_n}_REVERSE".format(_n=n+1)]):
					gm.players[n].states[1] = False
				elif e.key == eval(options["PLAYER{_n}_STEER_LEFT".format(_n=n+1)]):
					gm.players[n].states[2] = False
				elif e.key == eval(options["PLAYER{_n}_STEER_RIGHT".format(_n=n+1)]):
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
		ms = clock.tick(FPS) # Milliseconds after last tick
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
				if gm.number_of_humans == 2 and gm.number_of_players < 2:
					gm.set_number_of_players(2)
					race_options.components[2].index = 2 # Seting OptionChooser's value manually
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
			if gm.players:
				for n in range(gm.number_of_humans):
					gm.players[n].move()
				for player in gm.players:
					player.track_time(ms)
					if not player.reached_lap and player.crossed_lap:
						# Updating the texts of the player info panels.
						game_hud.player1_info_panel_labels[2].set_text(
							core.Text(str(gm.players[0].current_lap), game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC))
						game_hud.player1_info_panel_labels[4].set_text(
							core.Text(f"{gm.players[0].lap_timestamps[gm.players[0].current_lap][0]}:{gm.players[0].lap_timestamps[gm.players[0].current_lap][1]}:{gm.players[0].lap_timestamps[gm.players[0].current_lap][2]}", game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
						)
						if gm.number_of_humans == 2:
							game_hud.player2_info_panel_labels[2].set_text(
								core.Text(str(gm.players[1].current_lap), game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
							)
							game_hud.player2_info_panel_labels[4].set_text(
							core.Text(f"{gm.players[1].lap_timestamps[gm.players[1].current_lap][0]}:{gm.players[1].lap_timestamps[gm.players[1].current_lap][1]}:{gm.players[1].lap_timestamps[gm.players[1].current_lap][2]}", game_hud.FONT_SIZE, game_hud.COLOR, game_hud.FONT, game_hud.BOLD, game_hud.ITALIC)
						)

			for player in gm.players:
				if player.current_lap == gm.laps:
					if len(gm.players) > 0:
						results.components[1].set_text(f"{gm.players[0].lap_timestamps[gm.players[0].current_lap][0]}:{gm.players[0].lap_timestamps[gm.players[0].current_lap][1]}:{gm.players[0].lap_timestamps[gm.players[0].current_lap][2]}")
					if len(gm.players) > 1:
						results.components[4].set_text(f"{gm.players[1].lap_timestamps[gm.players[1].current_lap][0]}:{gm.players[1].lap_timestamps[gm.players[1].current_lap][1]}:{gm.players[1].lap_timestamps[gm.players[1].current_lap][2]}")
					if len(gm.players) > 2:
						results.components[7].set_text(f"{gm.players[2].lap_timestamps[gm.players[2].current_lap][0]}:{gm.players[2].lap_timestamps[gm.players[2].current_lap][1]}:{gm.players[2].lap_timestamps[gm.players[2].current_lap][2]}")
					if len(gm.players) > 3:
						results.components[10].set_text(f"{gm.players[3].lap_timestamps[gm.players[3].current_lap][0]}:{gm.players[3].lap_timestamps[gm.players[3].current_lap][1]}:{gm.players[3].lap_timestamps[gm.players[3].current_lap][2]}")
					if len(gm.players) > 4:
						results.components[13].set_text(f"{gm.players[4].lap_timestamps[gm.players[4].current_lap][0]}:{gm.players[4].lap_timestamps[gm.players[4].current_lap][1]}:{gm.players[4].lap_timestamps[gm.players[4].current_lap][2]}")
					gm.default()
					sm.change_scene(SceneManager.RESULTS)
				# gm.racing_positions[player.name] = player.get_time_to_clear_laps()
				# sorted_by_value = sorted(gm.racing_positions.items(), key=lambda kv: kv[1])

			if gm.bots:
				for bot in gm.bots:
					bot.think(gm.difficulty)

			
