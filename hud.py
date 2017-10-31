from PyGameWidgets import core
from PyGameWidgets import widgets
from cfg import options

class HUD:

    SIZE = 8
    PLAYER_INFO_PANEL_LABELS = 7
    COLOR = core.WHITE
    BORDER_COLOR = (255, 255, 255, 150)
    BORDER_WIDTH = 1
    FONT = "monospace"
    FONT_SIZE = 16
    BOLD = False
    ITALIC = False

    def __init__(self, gm):
        self.gm = gm
        self.panel = widgets.Panel(core.Grid((HUD.SIZE, HUD.SIZE), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
        self.player1_info_panel = widgets.Panel(core.Grid((2, HUD.PLAYER_INFO_PANEL_LABELS), self.panel.grid.cell_size), self.panel, (0, 0), None)
        self.player1_info_panel_labels = [
            widgets.TextLabel(
                self.player1_info_panel, 
                (0, 0), 
                core.Text("Player1", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (0, 1), 
                core.Text("Speed: ", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (1, 1), 
                core.Text("")
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (0, 2), 
                core.Text("Gear: ", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (1, 2), 
                core.Text("")
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (0, 3), 
                core.Text("Angle: ", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (1, 3), 
                core.Text("")
            )
        ]
        self.player2_info_panel = widgets.Panel(core.Grid((2, HUD.PLAYER_INFO_PANEL_LABELS), self.panel.grid.cell_size), self.panel, (1, 0), None)
        self.player2_info_panel_labels = [
            widgets.TextLabel(
                self.player2_info_panel, 
                (0, 0), 
                core.Text("Player2", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player2_info_panel, 
                (0, 1), 
                core.Text("Speed: ", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player2_info_panel, 
                (1, 1), 
                core.Text("")
            ),
            widgets.TextLabel(
                self.player2_info_panel, 
                (0, 2), 
                core.Text("Gear: ", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player2_info_panel, 
                (1, 2), 
                core.Text("")
            ),
            widgets.TextLabel(
                self.player2_info_panel, 
                (0, 3), 
                core.Text("Angle: ", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player2_info_panel, 
                (1, 3), 
                core.Text("")
            )
        ]
        self.player1_info_panel_labels[0].set_span((1, 0))
        [label.set_border(HUD.BORDER_COLOR, HUD.BORDER_WIDTH) for label in self.player1_info_panel_labels if label.text.value != "Player1"]
        [label.set_color(core.TRANSPARENT) for label in self.player1_info_panel_labels]
        self.player2_info_panel_labels[0].set_span((1, 0))
        [label.set_border(HUD.BORDER_COLOR, HUD.BORDER_WIDTH) for label in self.player2_info_panel_labels if label.text.value != "Player2"]
        [label.set_color(core.TRANSPARENT) for label in self.player2_info_panel_labels]

    def draw(self, surface):
        for label in self.player1_info_panel_labels:
            label.draw(surface)
        if self.gm.number_of_humans == 2:
            for label in self.player2_info_panel_labels:
                label.draw(surface)