import traceback
import tkinter as tk
import tkinter.filedialog as fd
import sys
import os
import pickle

class App(tk.Tk):

	def __init__(self, master=None):
		tk.Tk.__init__(self)
		self.title("Track Editor")
		self.grid()
		self.create_widgets()
		self.tracks_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tracks")
		self.track_size = 16
		self.file = {
			"GROUND_DATA": [],
			"WAYPOINTS": [],
			"SPAWNPOINTS": [],
			"ACTORPOINTS": []
		}
	
	def open_file(self):
		name = fd.askopenfilename(
			initialdir=self.tracks_path,
			filetypes=(("Track File", "*.trk"), ("All Files", "*.*")),
			title="Choose a track file to open."
		)
		print(name)
		try:
			with open(name, 'r') as _file:
				print(_file.read())
		except:
			print("No file exists")

	def save_file(self):
		f = fd.asksaveasfile(
			initialdir=self.tracks_path,
			filetypes=(("Track File", "*.trk"), ("All Files", "*.*")),
			defaultextension=".trk",
			title="Name a file to save.",
			mode="wb"
		)
		try:
			pickle.dump(self.file, f)
		except Exception as e:
			print("Save failed.")
			print(e)

	def create_widgets(self):
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

		self.menu_bar = tk.Menu(self)
		self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
		self.file_menu.add_command(label="Open", command=self.open_file)
		self.file_menu.add_command(label="Save", command=self.save_file)
		self.file_menu.add_separator()
		self.file_menu.add_command(label="Exit", command=self.quit)
		self.menu_bar.add_cascade(label="File", menu=self.file_menu)
		self.config(menu=self.menu_bar)

		self.content_selection_frame = tk.Frame(self)
		self.content_selection_frame.rowconfigure(0, weight=1)
		[self.content_selection_frame.columnconfigure(n, weight=1) for n in range(4)]
		self.content_selection_frame.grid(row=0, column=0, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
		self.content_selection_states = [False, False, False, False]
		self.ground_data_editor_button = tk.Button(self.content_selection_frame, text="Ground Data", 
			command=self.compose_ground_data_editor
		)
		self.ground_data_editor_button.grid(row=0, column=0, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
		self.waypoints_button = tk.Button(self.content_selection_frame, text="Waypoints", 
			command=None
		)
		self.waypoints_button.grid(row=0, column=1, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
		self.spawnpoints_button = tk.Button(self.content_selection_frame, text="Spawnpoints",
			command=None
		)
		self.spawnpoints_button.grid(row=0, column=2, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
		self.actorpoints_button = tk.Button(self.content_selection_frame, text="Actorpoints", 
			command=None
		)
		self.actorpoints_button.grid(row=0, column=3, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
		self.content_frame = tk.Frame(self)
		self.content_frame.rowconfigure(0, weight=1)
		self.content_frame.columnconfigure(0, weight=1)
		
	def compose_general_values_list(self, frame, _dict):
		self.values_list_box = tk.Listbox(frame)
		self.values_list_box.grid(row=0, column=1, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
		[self.values_list_box.insert(0, v) for v in _dict.keys()]

	def compose_ground_data_editor(self):
		self.ground_data_values = {
			"Nebulosa": 1,
			"Arcpath": 2
		}
		if not self.content_selection_states[0]:
			self.content_selection_states[0] = True
			self.content_frame.grid(row=1, column=0, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
			self.ground_data_editor_button.config(relief="sunken")
			self.ground_data_frame = tk.Frame(self.content_frame)
			self.ground_data_frame.rowconfigure(0, weight=1)
			[self.ground_data_frame.columnconfigure(n, weight=1) for n in range(self.track_size)]
			self.ground_data_frame.grid(row=0, column=0, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
			self.compose_general_values_list(self.content_frame, self.ground_data_values)
			self.ground_data_buttons = []
			# Have to deal with existent data.
			if not self.file["GROUND_DATA"]:
				print("Blah")
				for c in range(self.track_size):
					row = []
					row_data = []
					for r in range(self.track_size):
						button = tk.Button(
							self.ground_data_frame, 
							text=self.ground_data_values["Nebulosa"]
						)
						button.grid(row=r, column=c, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
						row.append(button)
						row_data.append(self.ground_data_values["Nebulosa"])
					self.ground_data_buttons.append(row)
					self.file["GROUND_DATA"].append(row_data) 
			else:
				for c in range(self.track_size):
					row = []
					for r in range(self.track_size):
						button = tk.Button(
							self.ground_data_frame, 
							text=self.ground_data[c][r]
						)
						button.grid(row=r, column=c, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
						row.append(button)
					self.ground_data_buttons.append(row)
			for r in self.ground_data_buttons:
				for b in r:
					b.config(command=lambda b=b: b.config(text=self.ground_data_values[self.values_list_box.get(tk.ACTIVE)]))
		else:
			self.content_selection_states[0] = False
			self.content_frame.grid_remove()
			self.ground_data_editor_button.config(relief="raised")

def main():
	
	app = App()
	app.mainloop()
		
	return 0

if __name__ == '__main__':
	main()