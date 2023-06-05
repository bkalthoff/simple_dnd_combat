# DND Combat

This program allows you to create movable units on a background image. You can add, remove, and modify units.
It's just a morning project on a day off for a dnd group I am in. Hope you find it useful.
I might keep adding to it, if you want to contribute, feel free to open a PR.

## Keybindings

- **Left-click**: Add an enemy unit.
- **Ctrl + Left-click**: Add a player unit.
- **Left-click and drag**: Start dragging a unit.
- **Right-click**: Remove a unit.
- **Mouse wheel**: Increase or decrease the size of the selected unit. (Ctrl + wheel changes the size of all units.)
- **Keyboard A-Z**: Set a character for the selected unit. If the character is already in use, it appends a number to make it unique.
- **Delete**: Toggle the "dead" state of the selected unit.
- **1**: Toggle the "prone" state of the selected unit.
- **2**: Toggle the "cursed" state of the selected unit.

## Usage

1. Select a background image when prompted.
2. Click the left mouse button to add enemies or players. Hold Ctrl while clicking to add a player.
3. Right-click a unit to remove it.
4. Drag units using the mouse.
5. Press A-Z to set a character for the selected unit.
6. Press Delete to toggle the "dead" state of the selected unit.
7. Press 1 to toggle the "prone" state of the selected unit.
8. Press 2 to toggle the "cursed" state of the selected unit.
9. Use the mouse wheel to resize the selected unit. Hold Ctrl while scrolling to resize all units.

## Build Instructions

To build the executable file using `venv` and `pyinstaller`, follow these steps:

1. Create a virtual environment:
	```
	python -m venv venv
	```
2. Activate the virtual environment:
- For Windows:
	```
	venv\Scripts\activate
	```
- For Unix/macOS:
	```
	source venv/bin/activate
	```
3. Install the required dependencies:
	```
	pip install -r requirements.txt
	```
4. Build the executable:
	```
	pyinstaller --onefile simple_dnd_combat/dnd_combat.py
	```
5. The executable file will be created in the `dist` directory.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.