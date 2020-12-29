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
            Config.dirs = self.file_content['dirs']
            Config.regex = self.file_content['regex']

            loguru.logger.success("Configuration file loaded")

        loguru.logger.info("App platforms to scrap: {platforms}", platforms=Config.platforms)
        loguru.logger.info("App entities to scrap: {entities}", entities=Config.entities)
        loguru.logger.info("App configuration directories: {dirs}", dirs=Config.dirs)
        loguru.logger.info("App regular expressions for parsing: {regex}", regex=Config.regex)
