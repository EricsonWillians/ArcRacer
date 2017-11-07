import traceback
import tkinter as tk
import sys

class App(tk.Tk):

	def __init__(self, master=None):
		tk.Tk.__init__(self)
		self.title("Track Editor")
		self.grid()
		self.create_widgets()
		self.track_size = 16
		
	def create_widgets(self):
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

		self.menu_bar = tk.Menu(self)
		self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
		self.file_menu.add_command(label="Open", command=None)
		self.file_menu.add_command(label="Save", command=None)
		self.file_menu.add_separator()
		self.file_menu.add_command(label="Exit", command=self.quit)
		self.menu_bar.add_cascade(label="File", menu=self.file_menu)
		self.config(menu=self.menu_bar)

		self.content_selection_frame = tk.Frame(self)
		self.content_selection_frame.rowconfigure(0, weight=1)
		self.content_selection_frame.columnconfigure(0, weight=1)
		self.content_selection_frame.grid(row=0, column=0, sticky=tk.NW+tk.W)
		self.content_selection_states = [False, False, False, False]
		self.ground_data_editor_button = tk.Button(self.content_selection_frame, text="Ground Data", command=self.compose_ground_data_editor)
		self.ground_data_editor_button.grid(row=0, column=0, sticky=tk.W)
		self.waypoints_button = tk.Button(self.content_selection_frame, text="Waypoints", command=None)
		self.waypoints_button.grid(row=0, column=1, sticky=tk.W)
		self.spawnpoints_button = tk.Button(self.content_selection_frame, text="Spawnpoints", command=None)
		self.spawnpoints_button.grid(row=0, column=2, sticky=tk.W)
		self.actorpoints_button = tk.Button(self.content_selection_frame, text="Actorpoints", command=None)
		self.actorpoints_button.grid(row=0, column=3, sticky=tk.W)
		self.content_frame = tk.Frame(self)
		self.content_frame.rowconfigure(0, weight=1)
		self.content_frame.columnconfigure(0, weight=1)
		
	def compose_ground_data_editor(self):
		self.ground_data_values = [
			"Nebulosa",
			"Arcpath"
		]
		if not self.content_selection_states[0]:
			self.content_selection_states[0] = True
			self.content_frame.grid(row=1, column=0, sticky=tk.N+tk.W+tk.S+tk.E)
			self.ground_data_editor_button.config(relief="sunken")
			self.ground_data_frame = tk.Frame(self.content_frame)
			self.ground_data_frame.rowconfigure(0, weight=1)
			self.ground_data_frame.columnconfigure(0, weight=1)
			self.ground_data_frame.grid(row=0, column=0, sticky=tk.N+tk.W+tk.S+tk.E)
			self.values_list_box = tk.Listbox(self.content_frame)
			self.values_list_box.grid(row=0, column=1, sticky=tk.N+tk.W+tk.S+tk.E)
			[self.values_list_box.insert(0, v) for v in self.ground_data_values]
			self.ground_data_spins = []
			for c in range(self.track_size):
				row = []
				for r in range(self.track_size):
					spin = tk.Button(self.ground_data_frame, text="0", command=None)
					spin.grid(row=r, column=c, sticky=tk.N+tk.W+tk.S+tk.E)
					row.append(spin)
				self.ground_data_spins.append(row)

		else:
			self.content_selection_states[0] = False
			self.content_frame.grid_remove()
			self.ground_data_editor_button.config(relief="raised")
			



		"""
		self.search_label = tk.Label(self, text="Search: ")
		self.search_label.grid(row=0, column=0, sticky=tk.N+tk.SW)
		self.search_entry = tk.Entry(self)
		self.search_entry.grid(row=0, column=0, padx=60, sticky=tk.N+tk.SW)
		self.content_area = tk.Text(self, wrap=tk.WORD)
		self.content_area.grid(row=1, column=0, sticky=tk.SW+tk.E)
		self.content_scroll_bar = tk.Scrollbar(self, command=self.content_area.yview)
		self.content_scroll_bar.grid(row=1, column=1, sticky=tk.NW+tk.S+tk.W)
		self.content_area["yscrollcommand"] = self.content_scroll_bar.set
				
		self.fetch_summary_button = tk.Button(self, text="Fetch summary", command=None)
		self.fetch_summary_button.grid(row=0, column=0, padx=232, sticky=tk.SW)
		self.fetch_page_button = tk.Button(self, text="Fetch page", command=None)
		self.fetch_page_button.grid(row=0, column=0, padx=352, sticky=tk.SW)
		self.fetch_html_button = tk.Button(self, text="Fetch HTML", command=None)
		self.fetch_html_button.grid(row=0, column=0, padx=446, sticky=tk.SW)
		self.fetch_images_button = tk.Button(self, text="Fetch images", command=None)
		self.fetch_images_button.grid(row=0, column=0, padx=546, sticky=tk.SW)
		self.quit_button = tk.Button(self, text="Quit", command=self.quit)
		self.quit_button.grid(row=2, column=0, sticky=tk.SW)
		"""

def main():
	
	app = App()
	app.mainloop()
		
	return 0

if __name__ == '__main__':
	main()