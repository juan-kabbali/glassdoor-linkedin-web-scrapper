import os
import re
import shutil
import sys
from datetime import datetime
from random import randrange

import click
import loguru
import setup
import pandas

from src.commands.LoadConfigCommand import LoadConfigFileCommand
from src.core import Logger, FilesHandler
from src.core.Config import Config
from src.parsers.BaseParser import BaseParser
from src.parsers.EnterpriseReviewParser import EnterpriseReviewParser
from src.parsers.EnterpriseParser import EnterpriseParser
from src.parsers.JobParser import JobParser


@click.command()
@click.option('-c', '--config-file', 'config_file', help="Path to config file")
@click.option('-a', '--analyse', 'is_analyse', is_flag=True, help="Extract all information from scrapped files")
@click.option('-C', '--classify', 'is_classify', is_flag=True, help="Classify files from source web to landing zone")
@click.option('-v', '--verbose', 'verbosity', count=True, help="Activate verbosity output")
@click.option('-V', '--version', 'is_version', is_flag=True, help="Print current version and stops execution")
@click.option('-t', '--test', 'is_test', is_flag=True, help="Dry run execution")
def main(config_file, is_analyse, is_classify, verbosity, is_version, is_test):

    if is_version:
        loguru.logger.success("You are running scrapper V.{version}", version=setup.version)
        exit(0)

    if not config_file:
        exit(loguru.logger.error("You must to pass a config file path with -c or --config-file flags"))

    LoadConfigFileCommand(file_path=config_file).execute()
    Logger.init_logger(verbosity)

    if is_classify:
        classify()

    if is_analyse:
        analyse()


def classify():
    """
    13546-AVIS-SOC-GLASSDOOR-E12966_P1.html
    {id_enterprise}-{content_type}-{platform}-{other}.html
    """
    loguru.logger.info("CLASSIFY COMMAND CALLED")
    list_files_expression = os.path.join(Config.dirs['web_source'], "*.html")
    files = FilesHandler.list_files(list_files_expression)
    regex = re.compile(Config.regex["file_name"])

    for file in files:

        matches = regex.search(file)

        destination = Config.dirs['landing_zone']
        destination = os.path.join(destination, Config.platforms[matches.group("platform").lower()]['path_name'])
        destination = os.path.join(destination, Config.entities[matches.group("content_type").lower()]['path_name'])

        shutil.copy(file, destination)
        loguru.logger.trace("File copied from {source} to {destination}", source=file, destination=destination)

    loguru.logger.success("All files have been copied successfully to landing zone")


def analyse():
    loguru.logger.info("ANALYZE COMMAND CALLED")
    for platform in Config.platforms:
        path = os.path.join(Config.dirs['landing_zone'], Config.platforms[platform]['path_name'])
        loguru.logger.trace("Analyzing {platform} landing zone at {path}", platform=platform.upper(), path=path)

        for entity in Config.entities:
            path = os.path.join(path, Config.entities[entity]['path_name'])
            loguru.logger.trace("Analyzing {entity} entity at {path}", entity=entity.upper(), path=path)
            files = FilesHandler.list_files(os.path.join(path, "*.html"))
            parser = globals()[Config.entities[entity]['parser']]
            parser_instance = parser()

            for file in files:
                parser_instance.file = file
                parser_instance.parse()
                parser_instance.extract_metadata()

            # write csv file with retrieved data
            csv_path = os.path.join(*[Config.dirs['curated_zone'],
                                      Config.platforms[platform]['path_name'],
                                      Config.entities[entity]['path_name'],
                                      f'{entity}.csv'])
            parser_instance.data_to_csv(csv_path, BaseParser.CSV_EXPORT['DATA'])

            # cleanup last path segment to next iteration
            path = os.path.dirname(path)

    # write csv file with file's metadata
    BaseParser.data_to_csv(None, os.path.join(Config.dirs['curated_zone'], 'metadata.csv'),
                           BaseParser.CSV_EXPORT['METADATA'])
