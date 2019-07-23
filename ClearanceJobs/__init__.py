import logging
from datetime import datetime
from dataclasses import dataclass

import requests


@dataclass
class ClearanceJobs:
    """[summary]

    [extended_summary]
    """
    username: str
    password: str
    url: str = 'https://api.clearancejobs.com/api/v1'

    def __post_init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.19.0)',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Mode': 'cors'
        })

    def get(self, route: str) -> requests.models.Response:
        url = "{}{}".format(self.url, route)
        resp = self.session.get(url)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(e)

        return resp

    def post(self, route: str, body: dict) -> requests.models.Response:
        """[summary]

        [extended_summary]

        Args:
            route (str): [description]
            body (dict): [description]

        Returns:
            requests.models.Response: [description]
        """
        url = "{}{}".format(self.url, route)
        resp = self.session.post(url, json=body)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(e)

        return resp

    def login(self) -> str:
        body = {
            "username": self.username,
            "password": self.password
        }
        resp = self.post('/auth/login', body)
        csrf = resp.json()['csrf_token']
        self.session.headers.update({
            'X-CSRF-TOKEN': csrf
        })
        logging.info('Logged in successfully')
        return csrf

    def get_user_profile(self, user_id):
        route = '/profiles/{}'.format(user_id)
        resp = self.get(route)
        return resp

    def parse_profile(self, data):
        #TODO: get email, phone, resume, etc
        pass

    def people_search(
        self,
        keyword: str,
        min_clearance: int=4,
        received: str="a"
    ) -> dict:
        """Search for people.

        This searches for people based on the criteria and returns a list of
        users in a dictionary.

        Args:
            keywords (str): A keyword used when seraching users.
            min_clearance (int, optional): Defaults to 4.
            received (str, optional): Defaults to "a".

        Returns:
            dict: [description]
        """

        body = {
            "min_clearance":min_clearance,
            "received":received,
            "keywords":keyword,
            "limit":25,
            "page":1,
            "sort_info":"timestamp desc"
        }
        resp = self.post('/resumes/search', body)
        data = resp.json()
        return data
