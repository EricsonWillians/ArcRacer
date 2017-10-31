from PyGameWidgets import core
from PyGameWidgets import widgets
from cfg import options

class HUD:

    SIZE = 8
    PLAYER1_INFO_PANEL_LABELS = 6
    COLOR = core.WHITE
    FONT = "monospace"
    FONT_SIZE = 16
    BOLD = False
    ITALIC = False

    def __init__(self):
        self.panel = widgets.Panel(core.Grid((HUD.SIZE, HUD.SIZE), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
        self.player1_info_panel = widgets.Panel(core.Grid((2, HUD.PLAYER1_INFO_PANEL_LABELS), self.panel.grid.cell_size), self.panel, (0, 0), None)
        self.player1_info_panel_labels = [
            widgets.TextLabel(
                self.player1_info_panel, 
                (0, 0), 
                core.Text("Speed: ", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (1, 0), 
                core.Text("")
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (0, 1), 
                core.Text("Gear: ", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (1, 1), 
                core.Text("")
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (0, 2), 
                core.Text("Angle: ", HUD.FONT_SIZE, HUD.COLOR, HUD.FONT, HUD.BOLD, HUD.ITALIC)
            ),
            widgets.TextLabel(
                self.player1_info_panel, 
                (1, 2), 
                core.Text("")
            )
        ]
        [label.set_color(core.TRANSPARENT) for label in self.player1_info_panel_labels]

    def draw(self, surface):
        for label in self.player1_info_panel_labels:
            label.draw(surface)