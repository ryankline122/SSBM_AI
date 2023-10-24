"""
This script helps find memory addresses that use pointers to other areas of memory.

This script only works when the emulator is running and a match is in-progress. 
"""
import dolphin_memory_engine._dolphin_memory_engine as dme
import configparser

def update_config(player_name, player_base_address):
    """
    This function reads from and updates the player values in config.ini. player_name should
    match the desired section name in the config file. 
    """
    # Create a ConfigParser object and read the config.ini file
    config = configparser.ConfigParser()
    config.read('python-stubs\MyScripts\config.ini')
    
    # Retrieve the new values from the get_player_addresses function
    player_addresses = get_player_addresses(player_base_address)

    # Update the values in the config.ini file
    config.set(player_name, 'Direction', player_addresses['direction_addr'])
    config.set(player_name, 'X', player_addresses['x_pos_addr'])
    config.set(player_name, 'Y', player_addresses['y_pos_addr'])
    config.set(player_name, 'isGrounded', player_addresses['is_grounded_addr'])
    config.set(player_name, 'Percentage', player_addresses['percentage_addr'])

    # Write the changes back to the config.ini file
    with open('python-stubs\MyScripts\config.ini', 'w') as configfile:
        config.write(configfile)


def get_player_addresses(player_base_address):
    """
    This function gets the final memory addresses of the following values. 
    
    Feel free to add to this if needed.
    """
    direction_addr = dme.follow_pointers(player_base_address, [0x2C, 0x2C])
    x_pos_addr = dme.follow_pointers(player_base_address, [0x2C, 0xB0])
    y_pos_addr = dme.follow_pointers(player_base_address, [0x2C, 0xB4])
    is_grounded_addr = dme.follow_pointers(player_base_address, [0x2C, 0xE0])
    percentage_addr = dme.follow_pointers(player_base_address, [0x2C, 0x1830])

    return {
        'direction_addr': hex(direction_addr).lstrip('0x'),
        'x_pos_addr': hex(x_pos_addr).lstrip('0x'),
        'y_pos_addr': hex(y_pos_addr).lstrip('0x'),
        'is_grounded_addr': hex(is_grounded_addr).lstrip('0x'),
        'percentage_addr': hex(percentage_addr).lstrip('0x')
    }


def setup():
    """
    DME must hook into the emulator before any operations can be performed.
    """
    while not dme.is_hooked():
        dme.hook()
        print("Attempting to hook")

    print("hooked")


if __name__ == "__main__":
    """
    Hooks into Dolpin, then updates the config file with the identified addresses for each
    player.
    """
    setup()

    try:
        # Player 1
        get_player_addresses(0x80453130)
        update_config("P1", 0x80453130)

        # Player 3
        get_player_addresses(0x80454E50)
        update_config('P3', 0x80454E50)
    except RuntimeError:
        print("ERROR: Make sure you have a match running. Addresses are set to 0 if not in use")
    