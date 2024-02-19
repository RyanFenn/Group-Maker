
import csv

CSV_FILE = 'players.csv'
HEADER_FIELD_NAMES_LIST = ['First Name', 'Last Name', 'Veteran Status', 'Skill Level (1 to 3)']

# - Creates a blank CSV file with a header. The file location is localized.
def create_blank_csv_with_header() -> None:
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)        
        writer.writerow(HEADER_FIELD_NAMES_LIST)

# - Creates / rewrites CSV file with header. The list of data is appended after the header. File location is localized.
# - alphabetically_sorted_list contains a list of players along with some information about the players. The list might
#       look something like this: [['Jack', 'Shephard', True, 3], ['John', 'Locke', True, 3]]
# - The list passed in should have the first names sorted alphabetically already.
def write_list_to_csv(alphabetically_sorted_list: list) -> None:
    create_blank_csv_with_header()

    with open(CSV_FILE, 'a', newline='') as file:
        for player_info in alphabetically_sorted_list:
            writer = csv.writer(file)        
            writer.writerow(player_info)

# - csv_file should be in the same directory as main.py.
# - CSV file must exist or an error will occur.
# - Returns players list.
def read_csv_to_list() -> list:
    with open(CSV_FILE, 'r', newline='') as file:   # 'r' means read. File must exist.
        reader = csv.reader(file)
        header = next(reader)   # The first line is the header

        data = []
        for row in reader:
            # row = [First Name, Last Name, Veteran Status, Skill (1 to 3)]
            first_name = row[0]
            last_name = row[1]
            is_veteran = True if row[2] == 'True' else False
            skill_level = int(row[3])

            data.append([first_name, last_name, is_veteran, skill_level])

        return data






