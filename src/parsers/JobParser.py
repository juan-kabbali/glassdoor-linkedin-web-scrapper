import loguru


from bs4 import BeautifulSoup
from src.core import FilesHandler
from src.parsers.BaseParser import BaseParser


class JobParser(BaseParser):

    def __int__(self, *args, **kwargs):
        super(JobParser, self).__int__(*args, **kwargs)
        loguru.logger.info("JOB PARSER INSTANTIATED")

    def parse(self):
        """
        Extracts following information from HTML file
        ✅ nom_entreprise
        ✅ nom_poste
        ✅ ville
        ✅ description_poste
        ✅ niveau_hierarchique
        ✅ type_emploi
        ✅ fonction
        ✅ secteurs
        """
        loguru.logger.trace("Job parse method called for file {file}", file=self.file)

        soup = BeautifulSoup(FilesHandler.load_file(self.file), "html.parser")
        # soup.encode('utf8')

        enterprise_name = soup.find('span', attrs={
            'class': 'topcard__flavor'
        }).text
        job_name = soup.find('h1', {
            'class': 'topcard__title'
        }).text
        city = soup.find('span', attrs={
            'class': 'topcard__flavor topcard__flavor--bullet'
        }).text
        job_description = soup.find('div', attrs={
            'class': 'description__text description__text--rich'
        }).text

        hierarchy_level = soup.find('h3', text="Niveau hiérarchique").next_sibling.text
        job_type = soup.find('h3', text="Type d’emploi").next_sibling.text

        functions = []
        for function in soup.find('h3', text="Fonction").next_siblings:
            functions.append(function.text)

        sectors = []
        try:
            for sector in soup.find('h3', text="Secteurs").next_siblings:
                sectors.append(sector.text)
        except AttributeError:
            loguru.logger.warning("file {file} has not 'secteurs' job information", file=self.file)

        row = {
            'id_enterprise': self.extract_id_enterprise(),
            'enterprise_name': enterprise_name,
            'job_name': job_name,
            'city': city,
            'job_description': job_description,
            'hierarchy_level': hierarchy_level,
            'job_type': job_type,
            'functions': functions,
            'sectors': sectors
        }

        # add current row to data instance
        self.data.append(row)
        self.print_row(row)

    def extract_metadata(self):
        loguru.logger.trace("Job metadata called for file {file}", file=self.file)
        super(JobParser, self).extract_metadata()
