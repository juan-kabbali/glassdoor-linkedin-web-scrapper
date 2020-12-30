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
        ✅ - recommande
        ✅ - point_de_vue
        ✅ - avis_pdg
        ✅ - type_employe
        ✅ - poste_employe
        ✅ - ville_employe
        ✅ - intro_avis
        ✅ - avantages_text_avis
        ✅ - inconvenients_text_avis
        ✅ - conseils_text_avis
        ✅ - nombre_utile
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
                loguru.logger.warning("One review of file {file} has not '{field_name}' score",
                                      file=self.file, field_name=field_name)
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
                loguru.logger.warning("One review of file {file} has not '{field_name}' score",
                                      file=self.file, field_name=field_name)

            score_recommend = score_point_of_view = score_pdg = None
            try:
                for recommend in review.find('div', attrs={'class': 'recommends'}).find_all('span'):
                    if 'recommande' in recommend.text.lower():
                        score_recommend = recommend.text

                    if 'vue' in recommend.text.lower():
                        score_point_of_view = recommend.text

                    if 'pdg' in recommend.text.lower():
                        score_pdg = recommend.text
            except AttributeError:
                loguru.logger.warning("One review of file {file} has not recommendations score", file=self.file)

            try:
                employee_city = soup.find('span', attrs={
                    'class': 'authorLocation'
                }).text
            except AttributeError:
                loguru.logger.warning("One review of file {file} has not employee city", file=self.file)
                employee_city = None

            employee_type = employee_job = None
            try:
                employee_data = soup.find('span', attrs={
                    'class': 'authorJobTitle'
                }).text.split('-')

                employee_type = employee_data[0].strip()
                employee_job = employee_data[1].strip()
            except IndexError:
                loguru.logger.warning("One review of file {file} has not complete employee data", file=self.file)

            review_intro = review.find('p', attrs={
                'class': 'mainText'
            }).text

            review_advantages = review_disadvantages = review_advises = None
            try:
                field_name = 'review_advantages'
                review_advantages = review.find('p', text="Avantages").next_sibling.text

                field_name = 'review_disadvantages'
                review_disadvantages = review.find('p', text="Inconvénients").next_sibling.text

                field_name = 'review_advises'
                review_advises = review.find('p', text="Conseils à la direction").next_sibling.text
            except AttributeError:
                loguru.logger.warning("One review of file {file} has not {field_name} data",
                                      file=self.file, field_name=field_name)

            useful_times = re.sub(r'[^\d]', '', review.find('button', attrs={
                'class': 'gd-ui-button'
            }).text).strip()

            useful_times = useful_times if useful_times else 0

            row = {
                'id_enterprise': self.extract_id_enterprise(),
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
                'score_recommend': score_recommend,
                'score_point_of_view': score_point_of_view,
                'score_pdg': score_pdg,
                'employee_type': employee_type,
                'employee_job': employee_job,
                'employee_city': employee_city,
                'review_intro': review_intro,
                'review_advantages': review_advantages,
                'review_disadvantages': review_disadvantages,
                'review_advises': review_advises,
                'useful_times': useful_times
            }

            # add current row to data instance
            self.data.append(row)
            self.print_row(row)

    def extract_metadata(self):
        loguru.logger.trace("Enterprise Review metadata called for file {file}", file=self.file)
        super(EnterpriseReviewParser, self).extract_metadata()
