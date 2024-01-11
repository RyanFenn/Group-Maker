
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
        self.unavailable_players_listbox = tk.Listbox(left_section_frame, activestyle='none', width=30, height=30)
        self.unavailable_players_listbox.grid(row=1, column=0, padx=20)

        self.potential_players_label = tk.Label(left_section_frame, text='Potential Players', font=('Arial', 14))
        self.potential_players_label.grid(row=0, column=1)
        self.potential_players_listbox = tk.Listbox(left_section_frame, activestyle='none', width=30, height=30)
        self.potential_players_listbox.grid(row=1, column=1, padx=20)

        self.available_label = tk.Label(left_section_frame, text='Available Players', font=('Arial', 14))
        self.available_label.grid(row=0, column=2)
        self.available_players_listbox = tk.Listbox(left_section_frame, activestyle='none', width=30, height=30)
        self.available_players_listbox.grid(row=1, column=2, padx=20)

        self.activate_potential_players_listbox_button = tk.Button(left_section_frame, text='Activate List', font=('Arial', 10),
            state='normal', command=self.activate_listbox_button_handling)
        self.activate_potential_players_listbox_button.grid(row=2, column=1, pady=15)

        self.activate_available_players_listbox_button = tk.Button(left_section_frame, text='Activate List', font=('Arial', 10),
            state='disabled', command=self.activate_listbox_button_handling)
        self.activate_available_players_listbox_button.grid(row=2, column=2, pady=15)

        self.update_availability_labels_and_listboxes()

    def activate_listbox_button_handling(self):
        if self.activate_available_players_listbox_button['state'] == 'normal':
            self.activate_available_players_listbox_button.config(state='disabled')
            self.activate_potential_players_listbox_button.config(state='normal')

        elif self.activate_potential_players_listbox_button['state'] == 'normal':
            self.activate_available_players_listbox_button.config(state='normal')
            self.activate_potential_players_listbox_button.config(state='disabled')

        self.update_availability_labels_and_listboxes()

    def update_availability_labels_and_listboxes(self):
        self.unavailable_label.config(bg='yellow')
        self.unavailable_players_listbox.config(state='normal', bg='white')

        if self.activate_potential_players_listbox_button['state'] == 'normal':
            self.available_label.config(bg='yellow')
            self.available_players_listbox.config(state='normal', bg='white')
            self.potential_players_label.config(bg='#f0f0f0')   # '#f0f0f0' is the default background color.
            self.potential_players_listbox.config(state='disabled', bg='#d9d9d9')   # '#d9d9d9' is a gray color.

            self.activate_available_players_listbox_button.grid_forget()   # Hides button.
            self.activate_potential_players_listbox_button.grid(row=2, column=1, pady=15)   # Adds button back in.

        elif self.activate_available_players_listbox_button['state'] == 'normal':
            self.potential_players_label.config(bg='yellow')
            self.potential_players_listbox.config(state='normal', bg='white')
            self.available_label.config(bg='#f0f0f0')   # '#f0f0f0' is the default background color.
            self.available_players_listbox.config(state='disabled', bg='#d9d9d9')   # '#d9d9d9' is a gray color.

            self.activate_potential_players_listbox_button.grid_forget()   # Hides button.
            self.activate_available_players_listbox_button.grid(row=2, column=2, pady=15)   # Adds button back in.

    # This section contains settings for player distribution and number of groups, and displays the current settings.
    # There are also buttons for editing player list and creating the groups here.
    def right_section(self) -> None:
        right_section_frame = tk.Frame(self.root)
        right_section_frame.grid(row=1, column=1, sticky='n', padx=20)

        distribution_frame = tk.LabelFrame(right_section_frame, text='Distribution Settings', font=('Arial', 14), bg='orange', labelanchor='n')
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

        number_of_groups_frame = tk.LabelFrame(right_section_frame, text='Number of Groups', font=('Arial', 14), bg='orange', labelanchor='n')
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
        number_of_gyms_frame = tk.LabelFrame(right_section_frame, text='Number of Gyms', font=('Arial', 14), bg='orange', labelanchor='n')
        number_of_gyms_frame.pack(pady=(20, 0))
        one_gym_radiobutton = tk.Radiobutton(number_of_gyms_frame, text='1 Gym', variable=self.number_of_gyms,
            value=1, font=('Arial', 12), command=self.update_number_of_gyms_label, state='normal')
        one_gym_radiobutton.grid(row=0, column=0, padx=5)
        two_gyms_radiobutton = tk.Radiobutton(number_of_gyms_frame, text='2 Gyms', variable=self.number_of_gyms,
            value=2, font=('Arial', 12), command=self.update_number_of_gyms_label)
        two_gyms_radiobutton.grid(row=0, column=1, padx=5)

        current_settings_frame = tk.LabelFrame(right_section_frame, text='Current Settings', font=('Arial', 14), bg='orange', labelanchor='n')
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

        buttons_frame = tk.Frame(right_section_frame, bg='orange', padx=5, pady=5)
        buttons_frame.pack(pady=(20, 0))
        edit_player_list_button = tk.Button(buttons_frame, text='Edit Player List', font=('Arial', 12), command=self.open_player_list_window)
        edit_player_list_button.grid(row=0, column=0, padx=10)
        create_groups_button = tk.Button(buttons_frame, text='Create Groups', font=('Arial', 12), bg='green', fg='white')
        create_groups_button.grid(row=0, column=1, padx=10)

    def update_number_of_groups_label(self) -> None:
        self.number_of_groups_label.config(text=f'Number of groups = {self.number_of_groups.get()}')

    def update_number_of_gyms_label(self) -> None:
        self.number_of_gyms_label.config(text=f'Number of gyms = {self.number_of_gyms.get()}')

    def open_player_list_window(self) -> None:
        player_list_popup_window = tk.Toplevel(self.root)
        player_list_popup_window.title('Edit Player List')

        # All widgets within this frame will get destroyed when rewriting the player list.
        self.player_list_frame = tk.Frame(player_list_popup_window)
        self.player_list_frame.pack()

        self.update_player_list_frame()

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
            self.player_list.append([current_first_name, current_last_name, self.is_veteran_leader.get(), self.skill_level.get()])
            self.player_list.sort()   # Sorts rows so the names are alphabetically organized.

            self.update_player_list_frame()
            csv_handling.write_list_to_csv(self.player_list)

    # - Removes a player from self.player_list, updates the player list window, and updates the CSV file.
    # - index -> This is the index of the value that is to be deleted from self.player_list.
    def remove_player(self, index: int) -> None:
        del self.player_list[index]
        self.update_player_list_frame()
        csv_handling.write_list_to_csv(self.player_list)

    # Destroys all widgets in the frame before creating widgets. This is done so that widgetes aren't written overtop of old widgets.
    def update_player_list_frame(self) -> None:

        # Destroy all widgets in the frame (clear the window).
        for widget in self.player_list_frame.winfo_children():
            widget.destroy()

        edit_player_list_title = tk.Label(self.player_list_frame, text='Edit Player List', font=('Arial', 20))
        edit_player_list_title.grid(row=0, column=0, columnspan=7)

        blank_space_holding_header_label = tk.Label(self.player_list_frame, width=5)
        blank_space_holding_header_label.grid(row=1, column=0)
        player_count_header_label = tk.Label(self.player_list_frame, text='Player Count', font=('Arial', 10))
        player_count_header_label.grid(row=1, column=1, padx=20)
        first_name_header_label = tk.Label(self.player_list_frame, text='First Name', font=('Arial', 10))
        first_name_header_label.grid(row=1, column=2, padx=20)
        last_name_header_label = tk.Label(self.player_list_frame, text='Last Name', font=('Arial', 10))
        last_name_header_label.grid(row=1, column=3, padx=20)
        is_veteran_leader_header_label = tk.Label(self.player_list_frame, text='Is Veteran/Leader', font=('Arial', 10))
        is_veteran_leader_header_label.grid(row=1, column=4, padx=20)
        skill_level_header_label = tk.Label(self.player_list_frame, text='Skill Level (1 to 3)', font=('Arial', 10))
        skill_level_header_label.grid(row=1, column=5, padx=20)

        for player_index in range(len(self.player_list)):

            # '#f73131' is red.
            player_removal_button = tk.Button(self.player_list_frame, text='Remove', font=('Arial', 6), bg='#f73131',
                command=lambda i=player_index: self.remove_player(i))
            player_removal_button.grid(row=player_index+2, column=0, padx=(20, 3), pady=1)

            line_background_color = '#f0f0f0'   # This is the default background color.
            if player_index % 2 == 0:   # If even number.
                line_background_color = '#d9d9d9'   # Gray.

            player_count_label = tk.Label(self.player_list_frame, text=player_index+1, font=('Arial', 10), bg=line_background_color)
            player_count_label.grid(row=player_index+2, column=1, sticky='nsew')
            first_name_label = tk.Label(self.player_list_frame, text=self.player_list[player_index][0], font=('Arial', 10), bg=line_background_color)
            first_name_label.grid(row=player_index+2, column=2, sticky='nsew')
            last_name_label = tk.Label(self.player_list_frame, text=self.player_list[player_index][1], font=('Arial', 10), bg=line_background_color)
            last_name_label.grid(row=player_index+2, column=3, sticky='nsew')
            is_veteran_leader_label = tk.Label(self.player_list_frame, text=str(self.player_list[player_index][2]), font=('Arial', 10), bg=line_background_color)
            is_veteran_leader_label.grid(row=player_index+2, column=4, sticky='nsew')
            skill_level_label = tk.Label(self.player_list_frame, text=self.player_list[player_index][3], font=('Arial', 10), bg=line_background_color)
            skill_level_label.grid(row=player_index+2, column=5, sticky='nsew')

        new_player_label = tk.Label(self.player_list_frame, text='New Player:', font=('Arial', 10))
        new_player_label.grid(row=len(self.player_list)+2, column=1, pady=25)
        self.first_name = tk.StringVar()
        self.first_name.set('')   # Empty string.
        first_name_entry_box = tk.Entry(self.player_list_frame, font=('Arial', 10), textvariable=self.first_name)
        first_name_entry_box.grid(row=len(self.player_list)+2, column=2, padx=10)
        self.last_name = tk.StringVar()
        self.last_name.set('')   # Empty string.
        last_name_entry_box = tk.Entry(self.player_list_frame, font=('Arial', 10), textvariable=self.last_name)
        last_name_entry_box.grid(row=len(self.player_list)+2, column=3, padx=10)

        self.first_name.trace_add('write', self.update_add_player_button_appearance)
        self.last_name.trace_add('write', self.update_add_player_button_appearance)

        self.is_veteran_leader = tk.BooleanVar()
        self.is_veteran_leader.set(False)
        is_veteran_leader_radiobuttons_frame = tk.LabelFrame(self.player_list_frame)
        is_veteran_leader_radiobuttons_frame.grid(row=len(self.player_list)+2, column=4, padx=10)
        is_veteran_leader_radiobutton_true = tk.Radiobutton(is_veteran_leader_radiobuttons_frame, text='True', font=('Arial', 10),
            variable=self.is_veteran_leader, value=True)
        is_veteran_leader_radiobutton_true.pack(side='left')
        is_veteran_leader_radiobutton_false = tk.Radiobutton(is_veteran_leader_radiobuttons_frame, text='False', font=('Arial', 10),
            variable=self.is_veteran_leader, value=False)
        is_veteran_leader_radiobutton_false.pack(side='left')

        self.skill_level = tk.IntVar()
        self.skill_level.set(3)
        skill_level_radiobutton_frame = tk.LabelFrame(self.player_list_frame)
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

        self.add_player_button = tk.Button(self.player_list_frame, text='Add Player', font=('Arial', 10), command=self.add_player)
        self.add_player_button.grid(row=len(self.player_list)+2, column=6, padx=10)
        self.update_add_player_button_appearance()




        

