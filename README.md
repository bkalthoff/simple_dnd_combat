# DND Combat

This program allows you to create movable sprites on a background image. You can add, remove, and modify sprites.

## Keybindings

- **Left-click**: Add an enemy.
- **Ctrl + Left-click**: Add a player.
- **Left-click and drag**: Start dragging a sprite.
- **Right-click**: Remove a sprite.
- **Mouse wheel**: Increase or decrease the size of the selected sprite. (Ctrl + wheel changes the size of all sprites.)
- **Keyboard A-Z**: Set a character for the selected sprite. If the character is already in use, it appends a number to make it unique.
- **Delete**: Toggle the "dead" state of the selected sprite.
- **1**: Toggle the "prone" state of the selected sprite.
- **2**: Toggle the "cursed" state of the selected sprite.

## Usage

1. Select a background image when prompted.
2. Click the left mouse button to add enemies or players. Hold Ctrl while clicking to add a player.
3. Right-click a sprite to remove it.
4. Drag sprites using the mouse.
5. Press A-Z to set a character for the selected sprite.
6. Press Delete to toggle the "dead" state of the selected sprite.
7. Press 1 to toggle the "prone" state of the selected sprite.
8. Press 2 to toggle the "cursed" state of the selected sprite.
9. Use the mouse wheel to resize the selected sprite. Hold Ctrl while scrolling to resize all sprites.

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
	pyinstaller --onefile main.py
	```
5. The executable file will be created in the `dist` directory.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.