from PyGameWidgets import core
from PyGameWidgets import widgets
from cfg import options

MENU_COLOR = core.WHITE
MENU_FONT = "monospace"
MENU_BOLD = True

class MainMenu:

    def __init__(self):
        self.panel = widgets.Panel(core.Grid((3, 9), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
        self.panel.set_color(core.BLACK)
        self.title = widgets.TextLabel(self.panel, (0, 0), core.Text("Rect Racer", 64, core.WHITE, "arial", True, True))
        self.title.text.font.set_bold(True)
        self.title.set_span((2, 1))
        self.buttons = [
            widgets.TextButton(self.panel, (1, 3), core.Text("Single Player", 32, MENU_COLOR, MENU_FONT, MENU_BOLD)),
            widgets.TextButton(self.panel, (1, 4), core.Text("Exit", 32, MENU_COLOR, MENU_FONT, MENU_BOLD))
        ]
        [b.set_color(core.BLACK) for b in self.buttons]
        [b.set_border(core.WHITE, 16) for b in self.buttons]

    def draw(self, surface):
        self.panel.draw(surface)
        self.title.draw(surface)
        [b.draw(surface) for b in self.buttons]

class RaceOptions:

    def __init__(self):
        self.panel = widgets.Panel(core.Grid((6, 9), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
        self.panel.set_color(core.BLACK)
        self.title = widgets.TextLabel(self.panel, (0, 0), core.Text("Race Options", 64, core.WHITE, "arial", True, True))
        self.title.text.font.set_bold(True)
        self.title.set_span((5, 1))
        self.components = [
            widgets.TextButton(self.panel, (1, 3), core.Text("Start Race", 32)),
            widgets.TextLabel(self.panel, (1, 4), core.Text("Players", 32)),
            widgets.OptionChooser(self.panel, (3, 4), [str(n) for n in range(1, 6)]),
            widgets.TextLabel(self.panel, (1, 5), core.Text("Humans", 32)),
            widgets.OptionChooser(self.panel, (3, 5), [str(n) for n in range(1, 3)]),
            widgets.TextButton(self.panel, (1, 6), core.Text("Return", 32))
        ]
        [c.set_color(core.BLACK) for c in self.components]
        [c.set_span((1, 0)) for c in self.components]
        [c.set_border(core.WHITE, 16) for c in self.components]

    def draw(self, surface):
        self.panel.draw(surface)
        self.title.draw(surface)
        [c.draw(surface) for c in self.components]

class PauseScreen:

    def __init__(self):
        self.panel = widgets.Panel(core.Grid((1, 1), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
        self.title = widgets.TextLabel(self.panel, (0, 0), core.Text("Paused", 64, core.WHITE, "arial", True, True))

    def draw(self, surface):
        self.title.draw(surface)