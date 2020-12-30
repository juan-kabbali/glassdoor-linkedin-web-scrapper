import re

import loguru
from bs4 import BeautifulSoup

from src.core import FilesHandler
from src.parsers.BaseParser import BaseParser


class EnterpriseReviewParser(BaseParser):

    def __init__(self, *args, **kwargs):
        super(EnterpriseReviewParser, self).__init__(*args, **kwargs)
        loguru.logger.info("ENTERPRISE REVIEW PARSER INSTANTIATED")

    def parse(self):
        """
        ✅ * nom_entreprise
        ✅ * score_moyen
        ✅  - titre_avis
        ✅ - date_avis
        ✅ - score_avis
        ✅ - score_equilibre
        ✅ - score_culture
        ✅ - score_opportunites
        ✅ - score_remuneration
        ✅ - score_equipe
           - recommande
           - point_de_vue
           - avis_pdg

           - type_employe
           - poste_employe
           - ville_employe
           - intro_avis
           - avantages_text_avis
           - inconvenients_text_avis
           - conseils_text_avis
           - nombre_utile
        """
        loguru.logger.trace("Enterprise Review parse method called for file {file}", file=self.file)

        soup = BeautifulSoup(FilesHandler.load_file(self.file), "html.parser")
        # soup.encode('utf8')

        enterprise_name = soup.find('span', id='DivisionsDropdownComponent').text
        score_avg = soup.find('div', {
            'class': 'v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large'
        }).text

        reviews = soup.find(id='ReviewsFeed').find_all('li', attrs={
            'class': 'empReview'
        })

        for review in reviews:

            title = re.sub(r'[«»]', '', review.find('a', {
                'class': 'reviewLink'
            }).text).strip()

            try:
                date = review.find('time')['datetime']
            except TypeError:
                loguru.logger.warning("file {file} has not '{field_name}' score", file=self.file, field_name=field_name)
                date = None

            score = review.find('span', attrs={
                'class': 'value-title'
            })['title']

            score_balanced = score_culture = score_opportunities = score_wage_advantages = score_leader_team = None
            try:
                field_name = 'score_balanced'
                score_balanced = review.find('div', text='Équilibre travail/vie privée').next_sibling['title']

                field_name = 'score_culture'
                score_culture = review.find('div', text='Culture et valeurs').next_sibling['title']

                field_name = 'score_opportunities'
                score_opportunities = review.find('div', text='Opportunités de carrière').next_sibling['title']

                field_name = 'score_wage_advantages'
                score_wage_advantages = review.find('div', text='Rémunération et avantages').next_sibling['title']

                field_name = 'score_leader_team'
                score_leader_team = review.find('div', text='Équipe dirigeante').next_sibling['title']

            except AttributeError:
                loguru.logger.warning("file {file} has not '{field_name}' score", file=self.file, field_name=field_name)


            row = {
                'enterprise_name': enterprise_name,
                'score_avg': score_avg,
                'title': title,
                'date': date,
                'score': score,
                'score_balanced': score_balanced,
                'score_culture': score_culture,
                'score_opportunities': score_opportunities,
                'score_wage_advantages': score_wage_advantages,
                'score_leader_team': score_leader_team,
            }

            # add current row to data instance
            self.data.append(row)

        # city = soup.find('span', attrs={
        #     'class': 'topcard__flavor topcard__flavor--bullet'
        # }).text
        # job_description = soup.find('div', attrs={
        #     'class': 'description__text description__text--rich'
        # }).text
        #
        # hierarchy_level = soup.find('h3', text="Niveau hiérarchique").next_sibling.text
        # job_type = soup.find('h3', text="Type d’emploi").next_sibling.text
        #
        # functions = []
        # for function in soup.find('h3', text="Fonction").next_siblings:
        #     functions.append(function.text)
        #
        # sectors = []
        # try:
        #     for sector in soup.find('h3', text="Secteurs").next_siblings:
        #         sectors.append(sector.text)
        # except AttributeError:
        #     loguru.logger.warning("file {file} has not 'secteurs' job information", file=self.file)
            self.print_row(row)

    def extract_metadata(self):
        loguru.logger.trace("Enterprise Review metadata called for file {file}", file=self.file)
        super(EnterpriseReviewParser, self).extract_metadata()
