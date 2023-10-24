# Super Smash Bros Melee AI
The goal of this project is to develop inteligent agents that play Super Smash Bros. Melee on the Dolphin Emulator.

## Getting Started
### Required Software
* Python3.11
* Felk’s fork of the dolphin emulator with Python Scripting support: https://github.com/Felk/dolphin/releases/tag/scripting-preview3 
* The lastest version of aldelaro5's dolphin memory engine: https://github.com/aldelaro5/Dolphin-memory-engine/tags
* A legally obtained copy of Super Smash Bros Melee

### Running Scripts in Dolphin
1. Open the directory containing the Dolphin executable (dolphin-scripting-preview3-x64)
2. Clone this repo in the root directory
3. Boot up the Dolphin executable and you should see the following: <br><br>
<img src="docs\ssbm1.PNG">

4. Click "Add New Script" and navigate to SSBM_AI/python-stubs/src and select "main.py"
5. It should now appear in "Running Scripts"
6. The script will now execute when you run the game.

If you want access to the log to see potential errors, warnings, or debug statements, in the toolbar click "View" --> "Show Log" and "Show Log Configuration". You should see new tabs next to the "Scripts" tab for both of these. Click on the "Log Configuration" tab and make sure to toggle on the "Scripting" checkbox.

Your logs will show up in the "Log" tab.

### Accessing Game Memory - Desktop Application
1. With the game up and running, run the Dolphin Memory Engine:

<img src="docs\mem.PNG">

2. To load in the game memory for SSBM, click File → Open, then navigate to the `python-stubs\Memory Files\` and select 
`SSBM NTSC 1.02.dmw`
3. You should now see 3 groups in the bottom window for global addresses, player data, and stage data. These sections store all known variables and their respective memory addresses. Run the game alongside this to see how the values change. 
4. Review the provided API within the folder `python-stubs/dolphin` to see how to programmatically access the game controller, memory, GUI, etc. This is how the agent will be interacting with the environment.

### Accessing Game Memory - Python Package
In addition to the desktop application, we can also use the dolphin memory engine (DME) through a python package. This will be particularly useful when working with multi-level pointers since these addresses don't stay constant. See `python-stubs\src\fetch_memory_addresses.py` for reference of how this is used.

All memory addresses (constant or not) are stored in `python-stubs\src\config.ini`

### Dealing with Pointers
For some variables, the memory address is a pointer that can have multiple levels and the final address is not always constant between games. For example, the (x,y) position is stored at a different address when playing on Battlefield vs Pokemon Stadium

To address this issue, you will want to run `python-stubs\src\fetch_memory_addresses.py` with the game running AND a match started. This script will write the current addresses to `config.ini`