import json
import os
import shutil
import jsonschema

class ConfigManager():
    def __init__(self, config_file_location, data_file_location, reset):
        """
        If we need args to take precedence over conf, do the merging in here
        As a rule, the program should never write to the config.json file
        If user wants to change a default setting, they should edit the file directly
        And if they want to override an option at  runtime, use a commandline arg

        data.json is expected to be written to, to save tracks as they're scanned for the first time by the user
        However, the user is also allowed to edit that file directly if they want
        """
        
        parent_dir = os.path.dirname(os.path.realpath(__file__))

        # todo: add warning in reset case
        # don't want people to accidentally lose their settings/library
        if not os.path.isfile(config_file_location) or reset:
            shutil.copyfile("{}/default_config.json".format(parent_dir), config_file_location)
        if not os.path.isfile(data_file_location) or reset:
            shutil.copyfile("{}/default_data.json".format(parent_dir), data_file_location)

        self.config_file_location = config_file_location
        self.data_file_location = data_file_location

        with open("{}/config_schema.json".format(parent_dir), 'r') as config_schema_file:
            config_schema = json.load(config_schema_file)

        with open(config_file_location, "r") as config_file:
            self.config = json.load(config_file)
        
        jsonschema.validate(instance=self.config, schema=config_schema)

        with open("{}/data_schema.json".format(parent_dir), 'r') as data_schema_file:
            self.data_schema = json.load(data_schema_file)

        with open(data_file_location, "r") as data_file:
            self.data = json.load(data_file)
        
        jsonschema.validate(instance=self.data, schema=self.data_schema)


    def write_data(self, barcode, track_locations):
        if barcode in self.data:
            raise Exception("tried to overwrite existing barcode data")
        self.data[barcode] = track_locations

        try:
            jsonschema.validate(instance=self.data, schema=self.data_schema)
        except jsonschema.ValidationError as e:
            raise jsonschema.ValidationError('Writing barcode: {}, for tracks: {}, didn\'t match schema'.format(barcode, track_locations)) from e

        # todo: before writting to data.json
        # read it again and check if there's any new data in there
        # that would be overwritten
        # (maybe user edited file directly while we were running)
        with open(self.data_file_location, 'w+') as data_file:
            json.dump(self.data, data_file, indent=4, sort_keys=True)

    def read_data(self, barcode):
        return self.data.get(barcode)

    def read_config(self, setting_name):
        return self.config[setting_name]