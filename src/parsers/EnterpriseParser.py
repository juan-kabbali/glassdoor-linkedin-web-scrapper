import html
import pprint
import re
import loguru
import unicodedata

from bs4 import BeautifulSoup
from src.core import FilesHandler
from src.parsers.BaseParser import BaseParser


class EnterpriseParser(BaseParser):

    def __init__(self, *args, **kwargs):
        super(EnterpriseParser, self).__init__(*args, **kwargs)
        loguru.logger.info("ENTERPRISE PARSER INSTANTIATED")

    def parse(self):
        """
        Extracts following information from HTML file
        ✅ nom_entreprise
        ✅ nombre_avis
        ✅ nombre_emplois
        ✅ nombre_salaires
        ✅ nombre_entretiens
        ✅ nombre_avantages
        ✅ nombre_photos
        ✅ site_web
        ✅ siege_social
        ✅ taille
        ✅ fonde
        ✅ type
        ✅ secteur
        ✅ revenu
        ✅ presentation
        ✅ number_distinctions_glassdoor
        ✅ distinctions_glassdoor
        ✅ prix
        ✅ number_prix
        """
        loguru.logger.trace("Enterprise parse metadata called for file {file}", file=self.file)

        soup = BeautifulSoup(FilesHandler.load_file(self.file), "html.parser")
        # soup.encode('utf8')

        enterprise_name = soup.find('span', id='DivisionsDropdownComponent').text
        number_reviews = soup.find('a', attrs={
            'data-label': 'Avis'
        }).findChild(attrs={
            'class': 'num h2'
        }).text
        number_jobs = soup.find('a', attrs={
            'data-label': 'Emplois'
        }).findChild(attrs={
            'class': 'num'
        }).text
        number_employees = soup.find('a', attrs={
            'data-label': 'Salaires'
        }).findChild(attrs={
            'class': 'num'
        }).text
        number_interviews = soup.find('a', attrs={
            'data-label': 'Entretiens'
        }).findChild(attrs={
            'class': 'num'
        }).text
        number_advantages = soup.find('a', attrs={
            'data-label': 'Avantages'
        }).findChild(attrs={
            'class': 'num'
        }).text
        number_photos = soup.find('a', attrs={
            'data-label': 'Photos'
        }).findChild(attrs={
            'class': 'num'
        }).text

        try:
            web_link = soup.find('span', attrs={
                'class': 'value website'
            }).findChild('a')['href']
        except AttributeError:
            loguru.logger.warning("file {file} has not 'web site link'", file=self.file)
            web_link = None

        try:
            city = soup.find('label', text="Siège social").next_sibling.text
        except AttributeError:
            loguru.logger.warning("file {file} has not 'city'", file=self.file)
            city = None

        try:
            size = soup.find('label', text="Taille").next_sibling.text
        except AttributeError:
            loguru.logger.warning("file {file} has not 'size'", file=self.file)
            size = None

        try:
            founding_date = soup.find('label', text="Fondé en").next_sibling.text
        except AttributeError:
            loguru.logger.warning("file {file} has not 'founding date'", file=self.file)
            founding_date = None

        try:
            enterprise_type = soup.find('label', text="Type").next_sibling.text
        except AttributeError:
            loguru.logger.warning("file {file} has not 'type'", file=self.file)
            enterprise_type = None

        try:
            sector = soup.find('label', text="Secteur").next_sibling.text
        except AttributeError:
            loguru.logger.warning("file {file} has not 'sector'", file=self.file)
            sector = None

        try:
            incomes = soup.find('label', text="Revenu").next_sibling.text
        except AttributeError:
            loguru.logger.warning("file {file} has not 'incomes'", file=self.file)
            incomes = None

        try:
            presentation = soup.find('div', attrs={
                'class': 'empDescription'
            })['data-full']
            presentation = BeautifulSoup(presentation, "html.parser").text
        except TypeError:
            loguru.logger.warning("file {file} has not 'presentation'", file=self.file)
            presentation = None

        distinctions = []
        number_distinctions = 0
        try:
            # parent p tag
            p_tags = soup.find('h3', text="Les distinctions Glassdoor").next_sibling.find_all('p', attrs={
                'class': 'noMargTop noMargBot'
            })
            number_distinctions = len(p_tags)
            for p in p_tags:
                distinction_tokens = unicodedata.normalize("NFKD", p.text).split(':')
                name = distinction_tokens[0].rstrip()

                for year_position in distinction_tokens[1].split(','):
                    year_position = year_position.strip()

                    distinction = {
                        'name': name,
                        'year': year_position.split(' ')[0],
                        'position': re.sub(r'[^\d]', '', year_position.split(' ')[1])
                    }
                    distinctions.append(distinction)

        except AttributeError:
            loguru.logger.warning("file {file} has not 'distinctions'", file=self.file)

        prizes = []
        try:
            for prize in soup.find_all('div', attrs={'class': 'award'}):
                prizes.append(prize.text) if prize.text not in prizes else prizes
            number_prizes = len(prizes)
        except AttributeError:
            loguru.logger.warning("file {file} has not 'prizes'", file=self.file)

        row = {
            'id_enterprise': self.extract_id_enterprise(),
            'enterprise_name': enterprise_name,
            'number_reviews': number_reviews,
            'number_jobs': number_jobs,
            'number_employees': number_employees,
            'number_interviews': number_interviews,
            'number_advantages': number_advantages,
            'number_photos': number_photos,
            'web_link': web_link,
            'city': city,
            'size': size,
            'founding_date': founding_date,
            'enterprise_type': enterprise_type,
            'sector': sector,
            'incomes': incomes,
            'presentation': presentation,
            'number_distinctions': number_distinctions,
            'distinctions': distinctions,
            'number_prizes': number_prizes,
            'prizes': prizes,
        }

        # add current row to data instance
        self.data.append(row)
        self.print_row(row)

    def extract_metadata(self):
        loguru.logger.trace("Enterprise metadata called for file {file}", file=self.file)
        super(EnterpriseParser, self).extract_metadata()
