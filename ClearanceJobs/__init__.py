import logging
from datetime import datetime
from dataclasses import dataclass

import requests


@dataclass
class ClearanceJobs:
    """Initialize ClearanceJobs class.

    Args:
        username (str): Username for clearance job
        password (str): Password for clearance job
        url (str): Default https://api.clearancejobs.com/api/v1. Specify API
        url. Only update if it changes.

    Attributes:
        session (request.Session): Session object for making requests.
    """
    username: str
    password: str
    url: str = 'https://api.clearancejobs.com/api/v1'

    def __post_init__(self):
        """Post Init.
        """
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.19.0)',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Mode': 'cors'
        })

    def get(self, route: str) -> requests.models.Response:
        """GET request wrapper for Clearance Jobs.

        Args:
            route (str): Route for the GET request.

        Returns:
            requests.models.Response: Response object.
        """
        url = "{}{}".format(self.url, route)
        resp = self.session.get(url)
        resp.raise_for_status()

        return resp.json()

    def post(self, route: str, body: dict) -> requests.models.Response:
        """POST request wrapper for Clearance Jobs.

        Args:
            route (str): Route for the POST request.
            body (dict): Body (data) for the POST request.

        Returns:
            requests.models.Response: Response Object.
        """
        url = "{}{}".format(self.url, route)
        resp = self.session.post(url, json=body)
        resp.raise_for_status()

        return resp.json()

    def login(self) -> str:
        """Login for Clearance Jobs API.

        Logs into Clearance Jobs and gets a csrf_token used for subsequent
        api calls.

        Returns:
            csrf (str): CSRF Token.
        """
        body = {
            "username": self.username,
            "password": self.password
        }
        resp = self.post('/auth/login', body)
        csrf = resp['csrf_token']
        self.session.headers.update({
            'X-CSRF-TOKEN': csrf
        })
        logging.info('Logged in successfully')
        return csrf

    def get_metadata(
        self,
        options=[
            'radius_op','received_op','poly_types_op','clearance_types_op',
            'job_type_op,career_level_op','edu_op','desired_salary_op',
            'state_op','relocate_op','location_us_op',
            'location_international_op','resume_sort_cj_search_op','indu_op'
        ]
    ):
        route = '/options/batch?options='
        for option in options:
           route = "{}{},".format(route,option)
        return self.get(route)

    def get_user_profile(self, user_id):
        route = '/profiles/{}'.format(user_id)
        return self.get(route)

    def parse_profile(self, data):
        #TODO: get email, phone, resume, etc
        pass

    def people_search(
        self,
        keyword: str,
        auto_paginate: bool=False,
        min_clearance: int=4,
        received: str="a",
        limit: int=25,
        page: int=1,
        sort_info: str="timestamp desc",
        **kwargs
    ) -> dict:
        """Search for people.

        This searches for people based on the criteria and returns a list of
        users in a dictionary.

        Args:
            keywords (str): A keyword used when seraching users.
            auto_paginate (bool): Defaults to False. Automatically get results
                from all pages and return in 1 dictionary.
            min_clearance (int, optional): Defaults to 4. Can get options from
                "get_metadata" method using "clearance_types_op" as an option.
            received (str, optional): Defaults to "a". Can get options from
                "get_metadata" method using "received_op" as an option.
            limit (int, optional): Defaults to 25. Specift a limit of people to
                return.
            page (int, option): Defaults to 1. Used for pagination. If more
                people are returned than the limit then there will be multiple
                pages.
            sort_info (str, option): Defaults to timestamp desc. Used for
                sorting the response of people.

        Returns:
            dict: Dictionary response from API return.
        """

        body = {
            "min_clearance":min_clearance,
            "received":received,
            "keywords":keyword,
            "limit":limit,
            "page":page,
            "sort_info":sort_info
        }
        if len(kwargs)>0:
            body.update(kwargs)

        data = self.post('/resumes/search', body)
        if auto_paginate:
            pages = data['meta']['pagination']['total_pages']
            if pages>1:
                for i in range(1,pages):
                    i = i + 1
                    body['page'] = i
                    temp_data = self.post('/resumes/search', body)
                    data['data'].extend(temp_data['data'])
        return data
