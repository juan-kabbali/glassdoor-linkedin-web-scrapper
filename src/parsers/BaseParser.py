import os
import re
import loguru
import pandas as pd

from abc import abstractmethod

from src.core.Config import Config


class BaseParser:

    CSV_EXPORT = {
        'METADATA': "metadata",
        'DATA': "data"
    }

    metadata = []

    def __init__(self, file=None):
        self.file = file
        self.data = []

    @abstractmethod
    def parse(self):
        pass

    def extract_metadata(self):
        """
        Extracts metadata from a file
        ✅ nom_original_fichier
        ✅ type
        ✅ id_entreprise
        ✅ format_original
        ✅ format_destination
        ✅ taille
        ✅ emplacement_original
        ✅ emplacement_destination
        ✅ web_source
        """

        regex = re.compile(Config.regex["file_name"])
        matches = regex.search(self.file)
        file_name = os.path.basename(self.file)

        row = {
            'file_name': file_name,
            'type': matches.group("content_type"),
            'id_enterprise': matches.group("id_enterprise"),
            'original_ext': 'html',
            'destination_ext': 'csv',
            'size': os.path.getsize(self.file) / 1000,
            'web_source': matches.group("platform"),
            'original_path': os.path.join(Config.dirs['web_source'], file_name),
            'destination_path': os.path.join(*[Config.dirs['landing_zone'],
                                               Config.platforms[matches.group("platform").lower()]['path_name'],
                                               Config.entities[matches.group("content_type").lower()]['path_name'],
                                               file_name])
        }

        BaseParser.metadata.append(row)

    def data_to_csv(self, full_path, source):
        path = os.path.dirname(full_path)
        if not os.path.exists(path):
            loguru.logger.warning("Path {path} created because it does not exists", path=path)
            os.mkdir(path)

        try:
            if source is BaseParser.CSV_EXPORT['DATA']:
                file_content = self.data
            if source is BaseParser.CSV_EXPORT['METADATA']:
                file_content = BaseParser.metadata

            df = pd.DataFrame(file_content)
            df.to_csv(full_path, encoding='utf-8')
            loguru.logger.success("CSV file written at {full_path}", full_path=full_path)
        except IOError:
            loguru.logger.exception(IOError)

    def print_row(self, row):
        loguru.logger.trace("{class_name} ROW: {row}", class_name=self.__class__.__name__, row=row)
