import json
import os
import shutil

class ConfigManager():
    def __init__(self, config_file_location, data_file_location):
        """
        If we need args to take precedence over conf, do the merging in here
        As a rule, the program should never write to the config.json file
        If user wants to change a default setting, they should edit the file directly
        And if they want to override an option at  runtime, use a commandline arg

        data.json is expected to be written to, to save tracks as they're scanned for the first time by the user
        However, the user is also allowed to edit that file directly if they want
        """
        
        parent_dir = os.path.dirname(os.path.realpath(__file__))

        if not os.path.isfile(config_file_location):
            shutil.copyfile("{}/default_config.json".format(parent_dir), config_file_location)
        if not os.path.isfile(data_file_location):
            shutil.copyfile("{}/default_data.json".format(parent_dir), data_file_location)

        self.config_file_location = config_file_location
        self.data_file_location = data_file_location

        with open(config_file_location, "r") as config_file:
            # todo: check schema
            self.config = json.load(config_file)
        with open(data_file_location, "r") as config_file:
            # todo: check schema
            self.data = json.load(config_file)


    def write_data(self, barcode, track_locations):
        if barcode in self.config:
            raise Exception("tried to overwrite existing barcode data")
        self.data[barcode] = track_locations
        # todo: before writting to data.json, read it again and check if there's any new data in there that would be removed (i.e. was not added by us)
        with open(self.data_file_location, 'w+') as data_file:
            json.dump(self.data, data_file, indent=4, sort_keys=True)

    def read_data(self, barcode):
        return self.data.get(barcode)

    def read_config(self, setting_name):
        return self.config[setting_name]