
import tkinter as tk
from tkinter import messagebox
import csv_handling

class GroupMakerGUI:
    def __init__(self) -> None:
        try:
            self.player_list = csv_handling.read_csv_to_list()

        except FileNotFoundError:
            print('File not found. Creating new CSV file.')
            csv_handling.create_blank_csv_with_header()
            self.player_list = []

        self.unavailable_players = self.player_list.copy()
        self.potential_players = []
        self.available_players = []

        self.root = tk.Tk()
        self.root.title('Group Maker')
        title_label = tk.Label(self.root, text='Group Maker', font=('Arial', 20))
        title_label.grid(row=0, column=0, columnspan=2)

        self.left_section()
        self.right_section()

        self.root.mainloop()

    # This section contains player availability listboxes and labels.
    def left_section(self) -> None:
        left_section_frame = tk.Frame(self.root)
        left_section_frame.grid(row=1, column=0)

        self.unavailable_label = tk.Label(left_section_frame, text='Unavailable Players', font=('Arial', 14))
        self.unavailable_label.grid(row=0, column=0)
        unavailable_players_listbox_frame = tk.Frame(left_section_frame)
        unavailable_players_listbox_frame.grid(row=1, column=0, padx=(30, 0))
        self.unavailable_players_listbox = tk.Listbox(unavailable_players_listbox_frame, activestyle='none', selectmode='single', width=30, height=30)
        self.unavailable_players_listbox.pack(side='left', fill='both')
        self.unavailable_players_scrollbar = tk.Scrollbar(unavailable_players_listbox_frame)
        self.unavailable_players_scrollbar.pack(side='right', fill='both')

        self.potential_players_label = tk.Label(left_section_frame, text='Potential Players', font=('Arial', 14))
        self.potential_players_label.grid(row=0, column=1)
        potential_players_listbox_frame = tk.Frame(left_section_frame)
        potential_players_listbox_frame.grid(row=1, column=1, padx=20)
        self.potential_players_listbox = tk.Listbox(potential_players_listbox_frame, activestyle='none', selectmode='single', width=30, height=30)
        self.potential_players_listbox.pack(side='left', fill='both')
        self.potential_players_scrollbar = tk.Scrollbar(potential_players_listbox_frame)
        self.potential_players_scrollbar.pack(side='right', fill='both')

        self.available_label = tk.Label(left_section_frame, text='Available Players', font=('Arial', 14))
        self.available_label.grid(row=0, column=2)
        available_players_listbox_frame = tk.Frame(left_section_frame)
        available_players_listbox_frame.grid(row=1, column=2)
        self.available_players_listbox = tk.Listbox(available_players_listbox_frame, activestyle='none', selectmode='single', width=30, height=30)
        self.available_players_listbox.pack(side='left', fill='both')
        self.available_players_scrollbar = tk.Scrollbar(available_players_listbox_frame)
        self.available_players_scrollbar.pack(side='right', fill='both')

        self.unavailable_players_listbox.bind('<<ListboxSelect>>', self.on_unavailable_listbox_select)
        self.potential_players_listbox.bind('<<ListboxSelect>>', self.on_potential_listbox_select)
        self.available_players_listbox.bind('<<ListboxSelect>>', self.on_available_listbox_select)

        self.activate_potential_players_listbox_button = tk.Button(left_section_frame, text='Activate List', font=('Arial', 10),
            state='normal', command=self.activate_listbox_button_handling)

        self.activate_available_players_listbox_button = tk.Button(left_section_frame, text='Activate List', font=('Arial', 10),
            state='disabled', command=self.activate_listbox_button_handling)

        self.update_availability_labels_and_listboxes()

    # - This is a callback function that gets called when an item is selected within the unavailable listbox.
    # - When a player name is selected from the listbox, it will be moved to a the other active listbox.
    def on_unavailable_listbox_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]

            # Copies the name to the other list and deletes the element from the original list.
            if self.activate_potential_players_listbox_button['state'] == 'disabled':   # This means potential players listbox is activated.
                self.potential_players.append(self.unavailable_players[index])
                del self.unavailable_players[index]

            elif self.activate_available_players_listbox_button['state'] == 'disabled':   # This means available players listbox is activated.
                self.available_players.append(self.unavailable_players[index])
                del self.unavailable_players[index]

            self.update_availability_labels_and_listboxes()

    # - This is a callback function that gets called when an item is selected within the potential listbox.
    # - When a player name is selected from the listbox, it will be moved to a the other active listbox.
    def on_potential_listbox_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]

            # Copies the name to the other list and deletes the element from the original list.
            self.unavailable_players.append(self.potential_players[index])
            del self.potential_players[index]

            self.update_availability_labels_and_listboxes()

    # - This is a callback function that gets called when an item is selected within the available listbox.
    # - When a player name is selected from the listbox, it will be moved to a the other active listbox.
    def on_available_listbox_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]

            # Copies the name to the other list and deletes the element from the original list.
            self.unavailable_players.append(self.available_players[index])
            del self.available_players[index]

            self.update_availability_labels_and_listboxes()

    def activate_listbox_button_handling(self):
        if self.activate_available_players_listbox_button['state'] == 'normal':
            self.activate_available_players_listbox_button.config(state='disabled')
            self.activate_potential_players_listbox_button.config(state='normal')

        elif self.activate_potential_players_listbox_button['state'] == 'normal':
            self.activate_available_players_listbox_button.config(state='normal')
            self.activate_potential_players_listbox_button.config(state='disabled')

        self.update_availability_labels_and_listboxes()

    # - Alphabetically sorts availability lists.
    def update_availability_labels_and_listboxes(self):
        self.unavailable_players.sort()
        self.potential_players.sort()
        self.available_players.sort()

        self.unavailable_players_listbox.config(state='normal', bg='white')

        # Don't need to keep track of the unavailable players listbox because it will never be disabled.
        state_potential_players_listbox = self.potential_players_listbox['state']
        state_available_players_listbox = self.available_players_listbox['state']

        # Change the state of these listboxes to 'normal' because disabled listboxes cannot be updated.
        # After modifying the listboxes, the listbox states will be changed back to their original state.
        self.potential_players_listbox.config(state='normal')
        self.available_players_listbox.config(state='normal')

        # Clear all names from listboxes before reloading them.
        self.unavailable_players_listbox.delete(0, 'end')
        self.potential_players_listbox.delete(0, 'end')
        self.available_players_listbox.delete(0, 'end')

        for i in range(len(self.unavailable_players)):
            # Insert first + last name into listbox
            self.unavailable_players_listbox.insert(i, f'{self.unavailable_players[i][0]} {self.unavailable_players[i][1]}')

        for i in range(len(self.potential_players)):
            self.potential_players_listbox.insert(i, f'{self.potential_players[i][0]} {self.potential_players[i][1]}')

        for i in range(len(self.available_players)):
            self.available_players_listbox.insert(i, f'{self.available_players[i][0]} {self.available_players[i][1]}')

        self.potential_players_listbox.config(state=state_potential_players_listbox)
        self.available_players_listbox.config(state=state_available_players_listbox)

        if self.activate_potential_players_listbox_button['state'] == 'normal':
            self.available_players_listbox.config(state='normal', bg='white')
            self.potential_players_label.config(bg='#f0f0f0')   # '#f0f0f0' is the default background color.
            self.potential_players_listbox.config(state='disabled', bg='#d9d9d9')   # '#d9d9d9' is a gray color.

            self.activate_available_players_listbox_button.grid_forget()   # Hides button.
            self.activate_potential_players_listbox_button.grid(row=2, column=1, padx=(70), pady=15, sticky='w')   # Adds button back in.

        elif self.activate_available_players_listbox_button['state'] == 'normal':
            self.potential_players_listbox.config(state='normal', bg='white')
            self.available_label.config(bg='#f0f0f0')   # '#f0f0f0' is the default background color.
            self.available_players_listbox.config(state='disabled', bg='#d9d9d9')   # '#d9d9d9' is a gray color.

            self.activate_potential_players_listbox_button.grid_forget()   # Hides button.
            self.activate_available_players_listbox_button.grid(row=2, column=2, padx=(50), pady=15, sticky='w')   # Adds button back in.

        self.unavailable_players_listbox.config(yscrollcommand=self.unavailable_players_scrollbar.set)
        self.unavailable_players_scrollbar.config(command=self.unavailable_players_listbox.yview)

        self.potential_players_listbox.config(yscrollcommand=self.potential_players_scrollbar.set)
        self.potential_players_scrollbar.config(command=self.potential_players_listbox.yview)

        self.available_players_listbox.config(yscrollcommand=self.available_players_scrollbar.set)
        self.available_players_scrollbar.config(command=self.available_players_listbox.yview)

    # This section contains settings for player distribution and number of groups, and displays the current settings.
    # There are also buttons for editing player list and creating the groups here.
    def right_section(self) -> None:
        right_section_frame = tk.Frame(self.root)
        right_section_frame.grid(row=1, column=1, sticky='n', padx=20)

        distribution_frame = tk.LabelFrame(right_section_frame, text='Distribution Settings', font=('Arial', 14), labelanchor='n')
        distribution_frame.pack(pady=(10, 0))
        even_veteran_distribution_state = tk.BooleanVar()   # Value is set to True so that checkbox defaults to checked.
        even_veteran_distribution_state.set(True)
        even_veteran_distribution_checkbutton = tk.Checkbutton(distribution_frame, text='Even Veteran/Leader Distribution', font=('Arial', 12),
            variable=even_veteran_distribution_state, width=30, anchor='w')
        even_veteran_distribution_checkbutton.pack()
        even_skill_level_distribution_state = tk.BooleanVar()
        even_skill_level_distribution_state.set(True)
        even_skill_level_distribution_checkbutton = tk.Checkbutton(distribution_frame, text='Even Skill Level Distribution', font=('Arial', 12),
            variable=even_skill_level_distribution_state, width=30, anchor='w')
        even_skill_level_distribution_checkbutton.pack()

        number_of_groups_frame = tk.LabelFrame(right_section_frame, text='Number of Groups', font=('Arial', 14), labelanchor='n')
        number_of_groups_frame.pack(pady=(20, 0))
        self.number_of_groups = tk.IntVar()
        self.number_of_groups.set(2)
        two_groups_radiobutton = tk.Radiobutton(number_of_groups_frame, text='2 Groups', variable=self.number_of_groups,
            value=2, font=('Arial', 12), command=self.update_number_of_groups_label)
        two_groups_radiobutton.grid(row=0, column=0, padx=5)
        three_groups_radiobutton = tk.Radiobutton(number_of_groups_frame, text='3 Groups', variable=self.number_of_groups,
            value=3, font=('Arial', 12), command=self.update_number_of_groups_label)
        three_groups_radiobutton.grid(row=1, column=0, padx=5)
        four_groups_radiobutton = tk.Radiobutton(number_of_groups_frame, text='4 Groups', variable=self.number_of_groups,
            value=4, font=('Arial', 12), command=self.update_number_of_groups_label)
        four_groups_radiobutton.grid(row=0, column=1, padx=5)
        five_groups_radiobutton = tk.Radiobutton(number_of_groups_frame, text='5 Groups', variable=self.number_of_groups,
            value=5, font=('Arial', 12), command=self.update_number_of_groups_label)
        five_groups_radiobutton.grid(row=1, column=1, padx=5)
        six_groups_radiobutton = tk.Radiobutton(number_of_groups_frame, text='6 Groups', variable=self.number_of_groups,
            value=6, font=('Arial', 12), command=self.update_number_of_groups_label)
        six_groups_radiobutton.grid(row=0, column=2, padx=5)

        self.number_of_gyms = tk.IntVar()
        self.number_of_gyms.set(1)
        number_of_gyms_frame = tk.LabelFrame(right_section_frame, text='Number of Gyms', font=('Arial', 14), labelanchor='n')
        number_of_gyms_frame.pack(pady=(20, 0))
        one_gym_radiobutton = tk.Radiobutton(number_of_gyms_frame, text='1 Gym', variable=self.number_of_gyms,
            value=1, font=('Arial', 12), command=self.update_number_of_gyms_label, state='normal')
        one_gym_radiobutton.grid(row=0, column=0, padx=5)
        two_gyms_radiobutton = tk.Radiobutton(number_of_gyms_frame, text='2 Gyms', variable=self.number_of_gyms,
            value=2, font=('Arial', 12), command=self.update_number_of_gyms_label)
        two_gyms_radiobutton.grid(row=0, column=1, padx=5)

        current_settings_frame = tk.LabelFrame(right_section_frame, text='Current Settings', font=('Arial', 14), labelanchor='n')
        current_settings_frame.pack(pady=(20, 0))
        number_of_available_players_label = tk.Label(current_settings_frame, text='Players available:',
            font=('Arial', 12), width=30, anchor='w')
        number_of_available_players_label.pack()
        min_number_of_players_per_group_label = tk.Label(current_settings_frame, text='Minimum players per group:',
            font=('Arial', 12), width=30, anchor='w')
        min_number_of_players_per_group_label.pack()
        self.number_of_groups_label = tk.Label(current_settings_frame, font=('Arial', 12), width=30, anchor='w')
        self.number_of_groups_label.pack()
        self.update_number_of_groups_label()
        self.number_of_gyms_label = tk.Label(current_settings_frame, font=('Arial', 12), width=30, anchor='w')
        self.number_of_gyms_label.pack()
        self.update_number_of_gyms_label()

        buttons_frame = tk.LabelFrame(right_section_frame, padx=5, pady=5)
        buttons_frame.pack(pady=(20, 0))
        self.edit_player_list_button = tk.Button(buttons_frame, text='Edit Player List', font=('Arial', 12), command=self.open_player_list_window)
        self.edit_player_list_button.grid(row=0, column=0, padx=10)
        create_groups_button = tk.Button(buttons_frame, text='Create Groups', font=('Arial', 12), bg='green', fg='white')
        create_groups_button.grid(row=0, column=1, padx=10)

    def update_number_of_groups_label(self) -> None:
        self.number_of_groups_label.config(text=f'Number of groups = {self.number_of_groups.get()}')

    def update_number_of_gyms_label(self) -> None:
        self.number_of_gyms_label.config(text=f'Number of gyms = {self.number_of_gyms.get()}')

    # - Opens a popup window to allow the user to see the current player list and make adjustments.
    # - To get a scrollbar for the player list window, some tricky coding needed to be done as a workaround
    #       because tkinter doesn't allow scrollbars to be used directly with a frame. Instead, an outer frame
    #       needed to be created, and then a canvas needed to be put inside that frame because a canvas is
    #       scrollable, and then the inner frame needed to be placed inside the canvas.
    def open_player_list_window(self) -> None:
        self.edit_player_list_button.config(state='disabled')
        self.player_list_popup_window = tk.Toplevel(self.root)
        self.player_list_popup_window.geometry('928x608')

        # When the player list popup window is closed, execute the callback function.
        self.player_list_popup_window.protocol('WM_DELETE_WINDOW', self.on_player_list_window_closing)

        self.player_list_popup_window.title('Edit Player List')

        # This frame contains the canvas and the inner frame.
        player_list_outer_frame = tk.Frame(self.player_list_popup_window)
        player_list_outer_frame.pack(fill='both', expand=1)

        self.player_list_canvas = tk.Canvas(player_list_outer_frame, highlightthickness=0)   # Set the highlightthickness to 0 to hide the canvas border.
        self.player_list_canvas.pack(side='left', fill='both', expand=1)

        player_list_scrollbar = tk.Scrollbar(player_list_outer_frame, orient='vertical', command=self.player_list_canvas.yview)
        player_list_scrollbar.pack(side='right', fill='y')

        self.player_list_canvas.config(yscrollcommand=player_list_scrollbar.set)

        # All widgets within this frame will get destroyed when updating the player list.
        self.player_list_inner_frame = tk.Frame(self.player_list_canvas)
        self.player_list_inner_frame.pack()

        # Add the inner frame to a window in the canvas.
        self.player_list_canvas.create_window((0,0), window=self.player_list_inner_frame, anchor='nw')

        self.player_list_canvas.bind('<Configure>', lambda e: self.update_scroll_region())
        self.player_list_inner_frame.bind('<Configure>', lambda e: self.update_scroll_region())

        self.update_player_list_frame()

    # Updating the scroll region may be necessary when player names are added or removed from the player list
    # or when the window is resized.
    def update_scroll_region(self):
        self.player_list_inner_frame.update_idletasks()
        self.player_list_canvas.config(scrollregion = self.player_list_canvas.bbox('all'))

    # Turns the edit player list button back to normal and then destroys the player list popup window.
    def on_player_list_window_closing(self):
        self.edit_player_list_button.config(state='normal')
        self.player_list_popup_window.destroy()

    # - Makes sure that the entry boxes for the first and last name are not empty. If one or both of these
    #       entry boxes are empty, the add player button will be disabled.
    # - This method is called every time self.first_name and self.last_name are modified (using the entry boxes).
    #       This is done using the trace_add() method.
    def update_add_player_button_appearance(self, *args) -> None:
        if len(self.first_name.get()) != 0 and len(self.last_name.get()) != 0:
            self.add_player_button.config(state='normal', bg='#2b5ffc', fg='white')   # '#2b5ffc' is blue.
        else:
            self.add_player_button.config(state='disabled', bg='#b5baf5')   # '#b5baf5' is a faded light blue color.   

    # - Adds a player to self.player_list and sorts the new player alphabetically. The player list window and the CSV file are both updated.
    # - If a player name exists already, an error message will be given.
    # - The players first and last name will be formatted so the first letter in each word is capitalized, and the other letters are lowercase.
    # - The availability listboxes will also be updated to include the newly added name. The new names will be placed in the unavailable listbox.
    def add_player(self) -> None:
        # .title() capitalizes first letter of each word
        current_first_name = self.first_name.get().title()
        current_last_name = self.last_name.get().title()

        does_player_already_exist = False

        for player_index in range(len(self.player_list)):
            if self.player_list[player_index][0] == current_first_name and self.player_list[player_index][1] == current_last_name:
                does_player_already_exist = True
                messagebox.showerror('Error', 'Player name already exists.')
                break

        if does_player_already_exist == False:
            current_player_data = [current_first_name, current_last_name, self.is_veteran_leader.get(), self.skill_level.get()]

            self.player_list.append(current_player_data)
            self.player_list.sort()   # Sorts rows so the names are alphabetically organized.

            self.update_player_list_frame()
            csv_handling.write_list_to_csv(self.player_list)

            self.unavailable_players.append(current_player_data)   # Newly added player data always go to the unavailable list.
            self.update_availability_labels_and_listboxes()

    # - Removes a player from self.player_list, updates the player list window, and updates the CSV file.
    # - index -> This is the index of the value that is to be deleted from self.player_list.
    # - Removes the player from the availability listbox on the main page.
    def remove_player(self, index: int) -> None:

        # If the player that is to be removed exists in any of the availability lists, remove the name.
        if self.player_list[index] in self.unavailable_players:
            self.unavailable_players.remove(self.player_list[index])
        elif self.player_list[index] in self.potential_players:
            self.potential_players.remove(self.player_list[index])
        elif self.player_list[index] in self.available_players:
            self.available_players.remove(self.player_list[index])

        self.update_availability_labels_and_listboxes()

        del self.player_list[index]
        self.update_player_list_frame()
        csv_handling.write_list_to_csv(self.player_list)

    # Destroys all widgets in the frame before creating widgets. This is done so that widgetes aren't written overtop of old widgets.
    def update_player_list_frame(self) -> None:

        # Destroy all widgets in the frame (clear the window).
        for widget in self.player_list_inner_frame.winfo_children():
            widget.destroy()

        edit_player_list_title = tk.Label(self.player_list_inner_frame, text='Edit Player List', font=('Arial', 20))
        edit_player_list_title.grid(row=0, column=0, columnspan=7)
        blank_space_holding_header_label = tk.Label(self.player_list_inner_frame, width=5)
        blank_space_holding_header_label.grid(row=1, column=0)
        player_count_header_label = tk.Label(self.player_list_inner_frame, text='Player Count', font=('Arial', 10))
        player_count_header_label.grid(row=1, column=1, padx=20)
        first_name_header_label = tk.Label(self.player_list_inner_frame, text='First Name', font=('Arial', 10))
        first_name_header_label.grid(row=1, column=2, padx=20)
        last_name_header_label = tk.Label(self.player_list_inner_frame, text='Last Name', font=('Arial', 10))
        last_name_header_label.grid(row=1, column=3, padx=20)
        is_veteran_leader_header_label = tk.Label(self.player_list_inner_frame, text='Is Veteran/Leader', font=('Arial', 10))
        is_veteran_leader_header_label.grid(row=1, column=4, padx=20)
        skill_level_header_label = tk.Label(self.player_list_inner_frame, text='Skill Level (1 to 3)', font=('Arial', 10))
        skill_level_header_label.grid(row=1, column=5, padx=20)

        for player_index in range(len(self.player_list)):

            # '#f73131' is red.
            player_removal_button = tk.Button(self.player_list_inner_frame, text='Remove', font=('Arial', 6), bg='#f73131',
                command=lambda i=player_index: self.remove_player(i))
            player_removal_button.grid(row=player_index+2, column=0, padx=(20, 3), pady=1)

            line_background_color = '#f0f0f0'   # This is the default background color.
            if player_index % 2 == 0:   # If even number.
                line_background_color = '#d9d9d9'   # Gray.

            player_count_label = tk.Label(self.player_list_inner_frame, text=player_index+1, font=('Arial', 10), bg=line_background_color)
            player_count_label.grid(row=player_index+2, column=1, sticky='nsew')
            first_name_label = tk.Label(self.player_list_inner_frame, text=self.player_list[player_index][0], font=('Arial', 10), bg=line_background_color)
            first_name_label.grid(row=player_index+2, column=2, sticky='nsew')
            last_name_label = tk.Label(self.player_list_inner_frame, text=self.player_list[player_index][1], font=('Arial', 10), bg=line_background_color)
            last_name_label.grid(row=player_index+2, column=3, sticky='nsew')
            is_veteran_leader_label = tk.Label(self.player_list_inner_frame, text=str(self.player_list[player_index][2]), font=('Arial', 10), bg=line_background_color)
            is_veteran_leader_label.grid(row=player_index+2, column=4, sticky='nsew')
            skill_level_label = tk.Label(self.player_list_inner_frame, text=self.player_list[player_index][3], font=('Arial', 10), bg=line_background_color)
            skill_level_label.grid(row=player_index+2, column=5, sticky='nsew')

        new_player_label = tk.Label(self.player_list_inner_frame, text='New Player:', font=('Arial', 10))
        new_player_label.grid(row=len(self.player_list)+2, column=1, pady=25)
        self.first_name = tk.StringVar()
        self.first_name.set('')   # Empty string.
        first_name_entry_box = tk.Entry(self.player_list_inner_frame, font=('Arial', 10), textvariable=self.first_name)
        first_name_entry_box.grid(row=len(self.player_list)+2, column=2, padx=10)
        self.last_name = tk.StringVar()
        self.last_name.set('')   # Empty string.
        last_name_entry_box = tk.Entry(self.player_list_inner_frame, font=('Arial', 10), textvariable=self.last_name)
        last_name_entry_box.grid(row=len(self.player_list)+2, column=3, padx=10)

        self.first_name.trace_add('write', self.update_add_player_button_appearance)
        self.last_name.trace_add('write', self.update_add_player_button_appearance)

        self.is_veteran_leader = tk.BooleanVar()
        self.is_veteran_leader.set(False)
        is_veteran_leader_radiobuttons_frame = tk.LabelFrame(self.player_list_inner_frame)
        is_veteran_leader_radiobuttons_frame.grid(row=len(self.player_list)+2, column=4, padx=10)
        is_veteran_leader_radiobutton_true = tk.Radiobutton(is_veteran_leader_radiobuttons_frame, text='True', font=('Arial', 10),
            variable=self.is_veteran_leader, value=True)
        is_veteran_leader_radiobutton_true.pack(side='left')
        is_veteran_leader_radiobutton_false = tk.Radiobutton(is_veteran_leader_radiobuttons_frame, text='False', font=('Arial', 10),
            variable=self.is_veteran_leader, value=False)
        is_veteran_leader_radiobutton_false.pack(side='left')

        self.skill_level = tk.IntVar()
        self.skill_level.set(3)
        skill_level_radiobutton_frame = tk.LabelFrame(self.player_list_inner_frame)
        skill_level_radiobutton_frame.grid(row=len(self.player_list)+2, column=5, padx=10)
        skill_level_radiobutton_1 = tk.Radiobutton(skill_level_radiobutton_frame, text='1', font=('Arial', 10),
            variable=self.skill_level, value=1)
        skill_level_radiobutton_1.pack(side='left')
        skill_level_radiobutton_2 = tk.Radiobutton(skill_level_radiobutton_frame, text='2', font=('Arial', 10),
            variable=self.skill_level, value=2)
        skill_level_radiobutton_2.pack(side='left')
        skill_level_radiobutton_3 = tk.Radiobutton(skill_level_radiobutton_frame, text='3', font=('Arial', 10),
            variable=self.skill_level, value=3)
        skill_level_radiobutton_3.pack(side='left')

        self.add_player_button = tk.Button(self.player_list_inner_frame, text='Add Player', font=('Arial', 10), command=self.add_player)
        self.add_player_button.grid(row=len(self.player_list)+2, column=6, padx=10)
        self.update_add_player_button_appearance()







