# Group-Maker
An application for creating random groups for sports.

### Brief Application Guide:
- Select the players that will be attending the event, adjust settings, and then click "Create Groups".

### Features:
- After groups are generated, players can be manually swapped in the group display window.
- There is a button in the group display window that copies the current list of groups to the computers clipboard. From here, the list can be pasted into a message, text file, etc.
- This application can be run using the executable file located within the "dist" folder. Note that this file might not contain the latest updates.

### Installation and Execution Instructions:
- Download the zip folder from GitHub and extract.
- If running the application from the executable file, the file can be found within the "dist" folder. Note that a CSV file will be created when running the executable if no CSV file exists already.
- The application can also be run through Python/Pipenv. Use `pipenv install` to install the dependencies, and then use `pipenv run python main.py` to run the program.
- To ensure that the executable file is up to date, a new executable file can be created using Pyinstaller. To do this, run `pipenv run pyinstaller main.py --onefile -w`. The new executable file should be located in the "dist" folder. Note that the `-w` flag is used to prevent the command prompt from popping up in the background when the executable file is started.
- When running the executable on Windows, the file might be seen as a virus. One solution for this problem is to add the executable file path to an exclusion list so that Microsoft Defender Antivirus doesn't scan the file. To do this in Windows, search for "Virus & threat protection". Within the "Virus & threat protection settings" section, click on "Manage settings", and then in the "Exclusions" section, select "Add or remove exclusions". Add the executable file path. Note that this part is only necessary if Window's antivirus protection is giving warnings, etc.

### Screenshots:
![Alt text](images/main-window.png)
![Alt text](images/player-list-window.png)
![Alt text](images/groups-window.png)
