import os
import pprint

import yaml
import loguru

from src.commands.BaseCommand import BaseCommand
from src.core.Config import Config


class LoadConfigFileCommand(BaseCommand):

    def __init__(self, **kwargs):
        self.file_path = kwargs.get('file_path')
        self.file_content = None

    def execute(self):
        loguru.logger.info("LOAD CONFIG FILE COMMAND CALLED")

        if not os.path.isfile(self.file_path):
            exit(loguru.logger.error(f"Configuration file {self.file_path} does not exist"))
        else:
            loguru.logger.success("Configuration file exists")
            Config.path = self.file_path

        with open(self.file_path) as config_file:
            self.file_content = yaml.safe_load(config_file)

            Config.entities = self.file_content['entities']
            Config.platforms = self.file_content['platforms']

            Config.dir_web_source = self.file_content['dirs']['web_source']
            Config.dir_landing_zone = self.file_content['dirs']['landing_zone']
            Config.dir_curated_zone = self.file_content['dirs']['curated_zone']
            Config.dir_logger_output = self.file_content['dirs']['logger_output']

            loguru.logger.success("Configuration file loaded")

        loguru.logger.success("App platforms to scrap: {platforms}", platforms=Config.platforms)
        loguru.logger.success("App entities to scrap: {entities}", entities=Config.entities)
