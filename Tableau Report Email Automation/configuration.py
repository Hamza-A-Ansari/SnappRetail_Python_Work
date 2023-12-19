import configparser
import os

filename=r'config.ini'
config = configparser.ConfigParser()
config.read(filename)

sect_dict={}
for sect in config.sections():
    
    config_dict = {}
    for k,v in config.items(sect):
        config_dict[k] = v
    sect_dict[sect] = config_dict

