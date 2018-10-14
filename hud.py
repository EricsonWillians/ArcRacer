from PyGameWidgets import core
from PyGameWidgets import widgets
import json

with open("cfg.json") as f:
	options = json.load(f)

class HUD:

	WIDTH = 8
	HEIGHT = 8
	PLAYER_INFO_PANEL_LABELS = 8
	COLOR = core.WHITE
	BORDER_COLOR = (255, 255, 255, 150)
	BORDER_WIDTH = 3
	FONT = "monospace"
	FONT_SIZE = 18
	BOLD = True
	ITALIC = False

	def __init__(self, gm):
	    self.gm = gm
	    self.panel = widgets.Panel(core.Grid((HUD.WIDTH, HUD.HEIGHT), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
	    self.player1_info_panel = widgets.Panel(core.Grid((3, HUD.PLAYER_INFO_PANEL_LABELS), self.panel.grid.cell_size), self.panel, (1, 0), None)
	    self.player1_info_panel_labels = [
			widgets.TextLabel(
	            self.player1_info_panel, 
	            (0, 2), 
	            core.Text("Player 1", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
	        ),			
			widgets.TextLabel(
	            self.player1_info_panel, 
	            (0, 4), 
	            core.Text("Lap:", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
	        ),
	        widgets.TextLabel(
	            self.player1_info_panel, 
	            (2, 4), 
	            core.Text("", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
	        ),
			widgets.TextLabel(
	            self.player1_info_panel, 
	            (0, 6), 
	            core.Text("Time:", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
	        ),
	        widgets.TextLabel(
	            self.player1_info_panel, 
	            (2, 6), 
	            core.Text("", int(HUD.FONT_SIZE / 2), HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
	        )
	    ]
	    self.player2_info_panel = widgets.Panel(core.Grid((3, HUD.PLAYER_INFO_PANEL_LABELS), self.panel.grid.cell_size), self.panel, (HUD.WIDTH-3, 0), None)
	    self.player2_info_panel_labels = [
			widgets.TextLabel(
	            self.player2_info_panel, 
	            (0, 2), 
	            core.Text("Player 2", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
	        ),			
			widgets.TextLabel(
	            self.player2_info_panel, 
	            (0, 4), 
	            core.Text("Lap:", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
	        ),
	        widgets.TextLabel(
	            self.player2_info_panel, 
	            (2, 4), 
	            core.Text("", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
	        ),
			widgets.TextLabel(
	            self.player2_info_panel, 
	            (0, 6), 
	            core.Text("Time:", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
	        ),
	        widgets.TextLabel(
	            self.player2_info_panel, 
	            (2, 6), 
	            core.Text("", int(HUD.FONT_SIZE / 2), HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
	        )
	    ]
	    self.player1_info_panel_labels[0].set_span((1, 0))
	    [label.set_color(core.TRANSPARENT) for label in self.player1_info_panel_labels]
	    self.player2_info_panel_labels[0].set_span((1, 0))
	    [label.set_color(core.TRANSPARENT) for label in self.player2_info_panel_labels]

	def draw(self, surface):
	    for label in self.player1_info_panel_labels:
	        label.draw(surface)
	    if self.gm.number_of_humans == 2:
	        for label in self.player2_info_panel_labels:
	            label.draw(surface)
