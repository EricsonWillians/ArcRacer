from PyGameWidgets import core
from PyGameWidgets import widgets
from cfg import options

class MainMenu:

    def __init__(self):
        self.panel = widgets.Panel(core.Grid((3, 10), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
        self.panel.set_color(core.BLACK)
        self.title = widgets.TextLabel(self.panel, (0, 0), core.Text("Rect Racer", 64, core.WHITE, "arial", True, True))
        self.title.text.font.set_bold(True)
        self.title.set_span((2, 1))
        self.buttons = [
            widgets.TextButton(self.panel, (1, 3), core.Text("Start Game", 32)),
            widgets.TextButton(self.panel, (1, 4), core.Text("Exit", 32))
        ]
        [b.set_color(core.BLACK) for b in self.buttons]
        [b.set_border(core.WHITE, 16) for b in self.buttons]

    def draw(self, surface):
        self.panel.draw(surface)
        self.title.draw(surface)
        [b.draw(surface) for b in self.buttons]

class PauseScreen:

    def __init__(self):
        self.panel = widgets.Panel(core.Grid((1, 1), (options["RESOLUTION"][0], options["RESOLUTION"][1])), None, None, (0, 0))
        self.title = widgets.TextLabel(self.panel, (0, 0), core.Text("Paused", 64, core.WHITE, "arial", True, True))

    def draw(self, surface):
        self.title.draw(surface)