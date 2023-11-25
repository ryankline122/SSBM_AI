"""
Module containing helper functions for SSBM
"""
import configparser

config = configparser.ConfigParser()
config.read('C:\\Users\matth\PycharmProjects\AI_Final_Project\dolphin-scripting-preview3-x64\SSBM_AI\python-stubs\src\config.ini')

def get_value_at(config_section, config_field):
    """
    Returns a memory address from the config file in hex.
    """
    return int(config.get(config_section, config_field), 16)