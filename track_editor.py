import traceback
import tkinter as tk
import tkinter.filedialog as fd
import sys
import os
import pickle
from collections import OrderedDict, namedtuple

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
			"WAYPOINTS": {},
			"SPAWNPOINTS": [],
			"ACTORPOINTS": []
		}
	
	def open_file(self):
		name = fd.askopenfilename(
			initialdir=self.tracks_path,
			filetypes=(("Track File", "*.trk"), ("All Files", "*.*")),
			title="Choose a track file to open."
		)
		try:
			self.file = pickle.load(open(name, 'rb'))
		except Exception as e:
			print("No file exists")
			print(e)

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
		self.content_names_in_file = {
			0: "GROUND_DATA",
			1: "WAYPOINTS",
			2: "SPAWNPOINTS",
			3: "ACTORPOINTS"
		}
		self.editor_buttons = [
			tk.Button(self.content_selection_frame, text="Ground Data", 
				command=self.compose_ground_data_editor
			),
			tk.Button(self.content_selection_frame, text="Waypoints", 
				command=self.compose_waypoint_data_editor
			),
			tk.Button(self.content_selection_frame, text="Spawnpoints",
				command=self.compose_spawn_data_editor
			),
			tk.Button(self.content_selection_frame, text="Actorpoints", 
				command=self.compose_actor_data_editor
			)
		]
		[self.editor_buttons[n].grid(row=0, column=n, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S) for n in range(4)]
		# General frames that hold simple and complex data editors.
		# There's just a single complex data editor, but, *whatever*, the abstraction is valid 
		# and allows the implementation of more complex data editors in the future if we decide to get fancier.
		self.content_frames = [
			tk.Frame(self) for n in range(4) 
		]
		[frame.rowconfigure(0, weight=1) for frame in self.content_frames]
		[frame.columnconfigure(0, weight=1) for frame in self.content_frames]
		# Each simple data frame holds a matrix of buttons and a corresponding ListBox widget.
		# They're all acceced through a "content selection number", hence the "content_names_in_file" variable 
		# (so that we can link each visual matrix with their corresponding data matrix within the file for storage)
		self.simple_data_frames = {}
		self.simple_data_buttons = {}
		self.simple_values_boxes = {}
		self.complex_data_frames = {}
		self.complex_data_selector_buttons = {}
		self.complex_data_selector_states = {}
		self.complex_data_selector_controller_buttons = {}
		self.complex_data_buttons = {}
		self.complex_values_boxes = {}
		
	def deselect_irrelevant_editors(self, content_selection_state_index):
		for i in range(len(self.content_selection_states)):
			if i != content_selection_state_index:
				self.content_selection_states[i] = False
				self.content_frames[i].grid_remove()
				self.editor_buttons[i].config(relief="raised")

	# Method that composes the simple data editors,
	# which are "Ground Data", "Spawnpoints" and "Actorpoints".
	# It's a long abstraction, but the code is pretty much the same for all of them, hence my decision.
	def compose_simple_data_editor(self, content_selection_state_index, data_values, default_data_value=1):
		# The data_values dict gets ordered by value.
		data_values = OrderedDict(sorted(data_values.items(), key=lambda item: item[1], reverse=True))
		
		if not self.content_selection_states[content_selection_state_index]:
			self.deselect_irrelevant_editors(content_selection_state_index)
			self.content_selection_states[content_selection_state_index] = True
			self.content_frames[content_selection_state_index].grid(row=1, column=0, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
			self.editor_buttons[content_selection_state_index].config(relief="sunken")
			self.simple_data_frames[content_selection_state_index] = tk.Frame(self.content_frames[content_selection_state_index])
			self.simple_data_frames[content_selection_state_index].rowconfigure(0, weight=1)
			[self.simple_data_frames[content_selection_state_index].columnconfigure(n, weight=1) for n in range(self.track_size)]
			self.simple_data_frames[content_selection_state_index].grid(row=0, column=0, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
			
			self.simple_values_boxes[content_selection_state_index] = tk.Listbox(self.content_frames[content_selection_state_index])
			self.simple_values_boxes[content_selection_state_index].grid(row=0, column=1, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
			[self.simple_values_boxes[content_selection_state_index].insert(0, v) for v in data_values.keys()]
			self.simple_values_boxes[content_selection_state_index].config(width=0) # Reseting the ListBox width is important to fit the size of each value string.
			
			# Defaulting the selection to the first index of the ListBox.
			# If there's no explicit default value, it defaults to the last value inserted,
			# with no visual representation, which is misleading.
			self.simple_values_boxes[content_selection_state_index].select_set(0)
			self.simple_values_boxes[content_selection_state_index].activate(0)

			self.simple_data_buttons[content_selection_state_index] = []
			if not self.file[self.content_names_in_file[content_selection_state_index]]:
				for c in range(self.track_size):
					row = []
					row_data = []
					for r in range(self.track_size):
						button = tk.Button(
							self.simple_data_frames[content_selection_state_index], 
							text=default_data_value
						)
						button.grid(row=r, column=c, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
						row.append(button)
						row_data.append(default_data_value)
					self.simple_data_buttons[content_selection_state_index].append(row)
					self.file[self.content_names_in_file[content_selection_state_index]].append(row_data) 
			else:
				for c in range(self.track_size):
					row = []
					for r in range(self.track_size):
						button = tk.Button(
							self.simple_data_frames[content_selection_state_index], 
							text=self.file[self.content_names_in_file[content_selection_state_index]][c][r]
						)
						button.grid(row=r, column=c, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
						row.append(button)
					self.simple_data_buttons[content_selection_state_index].append(row)
			def save_alteration_within_the_matrix(b, r, c):
				self.file[self.content_names_in_file[content_selection_state_index]][r][c] = b["text"]
			for c in range(self.track_size):
				row = []
				for r in range(self.track_size):
					b = self.simple_data_buttons[content_selection_state_index][r][c]
					# Simulating multiline statements inside a lambda using a list.
					# I chose this solution in order to handle lambda scoping rules (Hence the default arguments).
					# When a button is clicked within the matrix, not only its text must be updated according to the selected value,
					# but the according matrix within the file must be updated so that it can be eventually saved.
					b.config(command=lambda b=b, r=r, c=c: [
						b.config(	
							text=data_values[self.simple_values_boxes[content_selection_state_index].get(tk.ACTIVE)]
						),
						save_alteration_within_the_matrix(b, r, c)
					])
		else:
			self.content_selection_states[content_selection_state_index] = False
			self.content_frames[content_selection_state_index].grid_remove()
			self.editor_buttons[content_selection_state_index].config(relief="raised")

	def compose_complex_data_editor(self, content_selection_state_index, data_values, default_data_value=1):
		self.complex_data_frames[content_selection_state_index] = {}
		self.complex_data_buttons[content_selection_state_index] = {}
		self.complex_values_boxes[content_selection_state_index] = {}
		if not self.content_selection_states[content_selection_state_index]:
			self.deselect_irrelevant_editors(content_selection_state_index)
			self.content_selection_states[content_selection_state_index] = True
			self.content_frames[content_selection_state_index].grid(row=1, column=0, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
			self.editor_buttons[content_selection_state_index].config(relief="sunken")
			self.file[self.content_names_in_file[content_selection_state_index]]["1"] = []
			self.complex_data_frames[content_selection_state_index]["1"] = tk.Frame(self.content_frames[content_selection_state_index])
			self.complex_data_frames[content_selection_state_index]["1"].rowconfigure(0, weight=1)
			[self.complex_data_frames[content_selection_state_index]["1"].columnconfigure(n, weight=1) for n in range(self.track_size)]
			self.complex_data_frames[content_selection_state_index]["1"].grid(row=1, column=0, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
			self.complex_data_buttons[content_selection_state_index]["1"] = []
			self.complex_values_boxes[content_selection_state_index]["1"] = tk.Listbox(self.content_frames[content_selection_state_index])
			self.complex_values_boxes[content_selection_state_index]["1"].grid(row=1, column=1, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
			[self.complex_values_boxes[content_selection_state_index]["1"].insert(0, v) for v in data_values]
			self.complex_values_boxes[content_selection_state_index]["1"].config(width=0) # Reseting the ListBox width is important to fit the size of each value string.
			def generate_data_button_matrix(selector_id):
				for c in range(self.track_size):
					row = []
					row_data = []
					for r in range(self.track_size):
						button = tk.Button(
							self.complex_data_frames[content_selection_state_index][selector_id], 
							text=selector_id
						)
						button.grid(row=r, column=c, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
						row.append(button)
						row_data.append(default_data_value)
					self.complex_data_buttons[content_selection_state_index][selector_id].append(row)
					self.file[self.content_names_in_file[content_selection_state_index]][selector_id].append(row) 
			self.complex_data_selector_buttons[content_selection_state_index] = [
				tk.Button(self.content_frames[content_selection_state_index], text="1", 
					command=lambda: generate_data_button_matrix("1") 
				)
			]
			self.complex_data_selector_states[content_selection_state_index] = [False]
			# DataSelector = namedtuple("DataSelector", "button")
			# Have to define a DataSelector.
			def control(action=0): # 0 = ADD, 1 == REMOVE
				if not action:
					b_text_n = int(self.complex_data_selector_buttons[content_selection_state_index][-1]["text"])
					next_number = b_text_n+1
					self.complex_data_selector_buttons[content_selection_state_index].append(
						tk.Button(self.content_frames[content_selection_state_index], text=next_number, 
							command=generate_data_button_matrix(str(b_text_n))
						)
					)
					self.complex_data_selector_states[content_selection_state_index].append(False)
					self.complex_data_selector_buttons[content_selection_state_index][-1].grid(row=0, column=next_number+1, sticky=tk.W)
				else:
					if len(self.complex_data_selector_buttons[content_selection_state_index]) > 1:
						self.complex_data_selector_buttons[content_selection_state_index][-1].grid_remove()
						self.complex_data_selector_buttons[content_selection_state_index].pop()
						self.complex_data_selector_states[content_selection_state_index].pop()
			SelectorController = namedtuple("SelectorController", "button")
			self.complex_data_selector_controller_buttons[content_selection_state_index] = (
				SelectorController(
					tk.Button(self.content_frames[content_selection_state_index], text="+", 
						command=lambda: control(0)
					)
				),
				SelectorController(
					tk.Button(self.content_frames[content_selection_state_index], text="-", 
						command=lambda: control(1)
					)
				)
			)
			self.complex_data_selector_controller_buttons[content_selection_state_index][0].button.grid(row=0, column=0, sticky=tk.W)
			self.complex_data_selector_controller_buttons[content_selection_state_index][1].button.grid(row=0, column=1, sticky=tk.W)
			self.complex_data_selector_buttons[content_selection_state_index][0].grid(row=0, column=2, sticky=tk.W)
			
		else:
			self.content_selection_states[content_selection_state_index] = False
			self.content_frames[content_selection_state_index].grid_remove()
			self.editor_buttons[content_selection_state_index].config(relief="raised")

	def compose_ground_data_editor(self):
		self.ground_data_values = {
			"Nebulosa": 1,
			"Arcpath": 2
		}
		self.compose_simple_data_editor(0, # 0, which stands for Ground Data within the selection states.
			self.ground_data_values, 
			self.ground_data_values["Nebulosa"]
		)

	def compose_waypoint_data_editor(self):
		self.waypoint_data_values = [n for n in range(100)]
		self.compose_complex_data_editor(1, # 0, which stands for Ground Data within the selection states.
			self.waypoint_data_values, 
			0
		)

	def compose_spawn_data_editor(self):
		self.spawn_data_values = {
			# It's somewhat stupid to store data like this,
			# but the default data structure is a dict, and it's more intuitive for the user.
			"FIRST": 1, 
			"SECOND": 2,
			"THIRD": 3,
			"FOURTH": 4,
			"FIFTH": 5
		}
		self.compose_simple_data_editor(2, # 2, which stands for Spawnpoints within the selection states.
			self.spawn_data_values, 
			0 # The default value is 0 because there's 
			  # no sense in placing spawnpoints everywhere on the grid.
		)

	def compose_actor_data_editor(self):
		self.actor_data_values = {
			"ARCFINISH": 1, 
			"ARCCHECKPOINT_UP": 2,
			"ARCCHECKPOINT_DOWN": 3,
			"ARCCHECKPOINT_LEFT": 4,
			"ARCCHECKPOINT_RIGHT": 5
		}
		self.compose_simple_data_editor(3, # 3, which stands for Actorpoints within the selection states.
			self.actor_data_values, 
			0 # The default value is 0 because there's also 
			  # no sense in placing actors everywhere on the grid by default.
		)

def main():
	
	app = App()
	app.mainloop()
		
	return 0

if __name__ == '__main__':
	main()