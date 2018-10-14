from PyGameWidgets import core
from PyGameWidgets import widgets
import json

with open("cfg.json") as f:
	options = json.load(f)

TITLE_SIZE = 64
MENU_SIZE = 32
RESULTS_SIZE = 16
MENU_COLOR = core.WHITE
MENU_FONT = "arial"
MENU_BOLD = True
MENU_ITALIC = False
RACE_OPTIONS_MENU_SIZE = 22
RACE_OPTIONS_MENU_COLOR = core.WHITE
RACE_OPTIONS_MENU_FONT = "arial"
RACE_OPTIONS_MENU_BOLD = True
RACE_OPTIONS_MENU_ITALIC = False

class MainMenu:

    def __init__(self):
        self.panel = widgets.Panel(core.Grid((3, 9), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
        self.panel.set_color(core.BLACK)
        self.title = widgets.TextLabel(self.panel, (0, 0), core.Text("ArcRacer", TITLE_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True))
        self.title.text.font.set_bold(True)
        self.title.set_alignment(widgets.TextLabel.ALIGN_CENTER)
        self.title.set_span((2, 1))
        self.buttons = [
            widgets.TextButton(self.panel, (1, 3), core.Text("Single Player", MENU_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD)),
            widgets.TextButton(self.panel, (1, 4), core.Text("Multiplayer", MENU_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD)),
            widgets.TextButton(self.panel, (1, 5), core.Text("Custom Game", MENU_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD)),
            widgets.TextButton(self.panel, (1, 6), core.Text("Exit", MENU_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD))
        ]
        [b.set_color(core.BLACK) for b in self.buttons]
        [b.set_alignment(widgets.TextLabel.ALIGN_CENTER) for b in self.buttons]
        [b.set_border(core.WHITE, 16) for b in self.buttons]

    def draw(self, surface):
        self.panel.draw(surface)
        self.title.draw(surface)
        [b.draw(surface) for b in self.buttons]

class RaceOptions:

    def __init__(self, gm):
        self.panel = widgets.Panel(core.Grid((6, 12), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
        self.panel.set_color(core.BLACK)
        self.title = widgets.TextLabel(self.panel, (0, 0), core.Text("Race Options", TITLE_SIZE, RACE_OPTIONS_MENU_COLOR, RACE_OPTIONS_MENU_FONT, RACE_OPTIONS_MENU_BOLD, MENU_ITALIC))
        self.title.text.font.set_bold(True)
        self.title.set_alignment(widgets.TextLabel.ALIGN_CENTER)
        self.title.set_span((5, 1))
        self.components = [
            widgets.TextButton(self.panel, (1, 3), core.Text("Start Race", RACE_OPTIONS_MENU_SIZE, RACE_OPTIONS_MENU_COLOR, RACE_OPTIONS_MENU_FONT, RACE_OPTIONS_MENU_BOLD, RACE_OPTIONS_MENU_ITALIC)),
            widgets.TextLabel(self.panel, (1, 4), core.Text("Players", RACE_OPTIONS_MENU_SIZE, RACE_OPTIONS_MENU_COLOR, RACE_OPTIONS_MENU_FONT, RACE_OPTIONS_MENU_BOLD, RACE_OPTIONS_MENU_ITALIC)),
            widgets.OptionChooser(self.panel, (3, 4), [str(n) for n in range(0, 6)]),
            widgets.TextLabel(self.panel, (1, 5), core.Text("Humans", RACE_OPTIONS_MENU_SIZE, RACE_OPTIONS_MENU_COLOR, RACE_OPTIONS_MENU_FONT, RACE_OPTIONS_MENU_BOLD, RACE_OPTIONS_MENU_ITALIC)),
            widgets.OptionChooser(self.panel, (3, 5), [str(n) for n in range(0, 3)]),
            widgets.TextLabel(self.panel, (1, 6), core.Text("Difficulty", RACE_OPTIONS_MENU_SIZE, RACE_OPTIONS_MENU_COLOR, RACE_OPTIONS_MENU_FONT, RACE_OPTIONS_MENU_BOLD, RACE_OPTIONS_MENU_ITALIC)),
            widgets.OptionChooser(self.panel, (3, 6), ["Easy", "Normal", "Hard", "Insane", "Arcturian"], 1),
            widgets.TextLabel(self.panel, (1, 7), core.Text("Laps", RACE_OPTIONS_MENU_SIZE, RACE_OPTIONS_MENU_COLOR, RACE_OPTIONS_MENU_FONT, RACE_OPTIONS_MENU_BOLD, RACE_OPTIONS_MENU_ITALIC)),
            widgets.OptionChooser(self.panel, (3, 7), ["5", "10", "15", "20", "25", "30", "35", "40", "45", "50"], 2),
            widgets.TextLabel(self.panel, (1, 8), core.Text("Track", RACE_OPTIONS_MENU_SIZE, RACE_OPTIONS_MENU_COLOR, RACE_OPTIONS_MENU_FONT, RACE_OPTIONS_MENU_BOLD, RACE_OPTIONS_MENU_ITALIC)),
            widgets.OptionChooser(self.panel, (3, 8), gm.get_track_list()),
            widgets.TextButton(self.panel, (1, 9), core.Text("Return", RACE_OPTIONS_MENU_SIZE, RACE_OPTIONS_MENU_COLOR, RACE_OPTIONS_MENU_FONT, RACE_OPTIONS_MENU_BOLD, RACE_OPTIONS_MENU_ITALIC))
        ]
        [c.set_color(core.BLACK) for c in self.components]
        [c.set_alignment(widgets.TextLabel.ALIGN_CENTER) if not isinstance(c, widgets.OptionChooser) else c.label.set_alignment(widgets.TextLabel.ALIGN_CENTER) for c in self.components]
        [
            c.set_span((1, 0)) if c != self.components[0] and c != self.components[len(self.components)-1] else c.set_span((3, 0)) for c in self.components
        ]
        [c.set_border(core.WHITE, 16) for c in self.components]

    def draw(self, surface):
        self.panel.draw(surface)
        self.title.draw(surface)
        [c.draw(surface) for c in self.components]

class Results:

	def __init__(self, gm):
		self.panel = widgets.Panel(core.Grid((6, 16), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
		self.panel.set_color(core.BLACK)

		self.title = widgets.TextLabel(self.panel, (1, 1), core.Text("Results ", TITLE_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True))
		self.title.set_span((3, 0))
		self.components = [
			widgets.TextLabel(self.panel, (1, 4), core.Text("Player 1: ", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (2, 4), core.Text("", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (3, 4), core.Text("", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (1, 5), core.Text("Player 2: ", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (2, 5), core.Text("", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (3, 4), core.Text("", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (1, 6), core.Text("Player 3: ", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (2, 6), core.Text("", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (3, 4), core.Text("", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (1, 7), core.Text("Player 4: ", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (2, 7), core.Text("", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (3, 4), core.Text("", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (1, 8), core.Text("Player 5: ", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (2, 8), core.Text("", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True)),
			widgets.TextLabel(self.panel, (3, 4), core.Text("", RESULTS_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD, True))
		]
		self.buttons = [
            widgets.TextButton(self.panel, (2, 12), core.Text("Restart", MENU_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD)),
            widgets.TextButton(self.panel, (2, 13), core.Text("Quit", MENU_SIZE, MENU_COLOR, MENU_FONT, MENU_BOLD))
        ]
		[b.set_color(core.BLACK) for b in self.buttons]
		[b.set_alignment(widgets.TextLabel.ALIGN_CENTER) for b in self.buttons]
		[b.set_span((1, 0)) for b in self.buttons]
		[b.set_border(core.WHITE, 4) for b in self.buttons]
		

	def draw(self, surface):
		self.panel.draw(surface)
		self.title.draw(surface)
		[c.draw(surface) for c in self.components]
		[b.draw(surface) for b in self.buttons]

class PauseScreen:

    def __init__(self):
        self.panel = widgets.Panel(core.Grid((1, 1), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
        self.title = widgets.TextLabel(self.panel, (0, 0), core.Text("Paused", 64, core.WHITE, "arial", True, True))

    def draw(self, surface):
        self.title.draw(surface)
