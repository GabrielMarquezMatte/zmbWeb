# -*- coding: utf-8 -*-

import requests
import json
import warnings
from os import environ
from requesterfactory import RequesterFactory
from dotenv import load_dotenv

load_dotenv()

"""
This module provides classes to interface with the Zumbi REST
API.

To make use of the Zumbi API, you need to obtain an API key by
contacting Jefferson O. Silva at silvajo@pucsp.br.
"""

__author__ = "Jefferson O. Silva"
__credits__ = "All the team"
__copyright__ = "Copyright 2021, PUC-SP Intelligence Team"
__version__ = "0.1"
__maintainer__ = "Jefferson O. Silva"
__email__ = "silvajo@pucsp.br"
__date__ = "January, 1, 2021"

class Rester(object):
    """
    A class to conveniently interface with the Stract REST interface.
    The recommended way to use our StractRester is with the "with" context
    manager to ensure that sessions are properly closed after usage::

        with StractRester("API_KEY") as m:
            do_something

    StractRester uses the "requests" package, which provides for HTTP connection
    pooling. All connections are made via https for security.

    Args:
        api_key (str): A String API key for accessing the Project
            REST interface. Please obtain your API key by emailing
            Jefferson O. Silva at silvajo@pucsp.br. If this is None,
            the code will check if there is a "STRACT_API_KEY" environment variable.
            If so, it will use that environment variable. This makes
            easier for heavy users to simply add this environment variable to
            their setups and MatstractRester can then be called without any arguments.
        endpoint (str): URL of endpoint to access the Zumbi REST
            interface. Defaults to the standard address, but can be changed to other
            urls implementing a similar interface.
    """

    def __init__(self, api_key:str|None=None, endpoint:str|None=None):
        self.api_key = api_key if api_key else environ.get('ZUMBI_API_KEY', None)
        if not self.api_key:
            raise ZumbiRestError(
                "Please specify an API key or request one through the "
                "Zumbi team."
            )

        if endpoint:
            self.preamble = endpoint
        else:
            endpoint = environ.get("ZUMBI_ENDPOINT")
            api_version =environ.get("ZUMBI_API_VERSION")
            api_base_path = f"{endpoint}{api_version}"
            self.preamble = api_base_path

        self.session = requests.Session()
        self.session.headers = {"x-api-key": self.api_key}

    def __enter__(self):
        """
        Support for "with" context.
        """
        return self

    def __exit__(self, *_):
        """
        Support for "with" context.
        """
        self.session.close()

    def _make_request(self, sub_url, payload=None, method="GET"):
        requester = RequesterFactory.create(self.session, "dummy")
        url = self.preamble + sub_url
        try:
            return requester.make_request(url, method, payload, True)
        except requests.HTTPError as ex:
            raise ZumbiRestError(ex.strerror)

    def __search(self, group_by, entities, text=None, elements=None, top_k=10):
        method = "POST"
        sub_url = "/search/"
        query = {'entities': entities, 'group_by': group_by, 'limit': top_k}
        if text:
            query['text'] = text
        if elements:
            query['elements'] = elements

        return self._make_request(sub_url, payload=query, method=method)

    # Public Methods
    # ==========================================================================

    def entities_search(self, entities, text=None, elements=None, top_k=10):
        method = "GET"
        sub_url = "stats/entities"
        query = entities

        return self._make_request(sub_url, payload=query, method=method)

    def entities_summary(self, entities, text=None, elements=None, top_k=10):
        method = "GET"
        sub_url = "stats/summary"
        query = None

        return self._make_request(sub_url, payload=query, method=method)

    def abstracts_search(self, entities, text=None, elements=None, top_k=10):
        """
        Search for news by entities and text filters.

        Args:

            entities: dict of entity lists (list of str) to filter by. Keys are
              singular snake case for each of the entity types (entity types list)

            text: english text, which gets searched on via Elasticsearch.

            elements: string or list of strings; filter by elements

            top_k: (int or None) if int, specifies the number of matches to
                return; if None, returns all matches.

        Returns:
            List of entries (dictionaries) with abstracts, entities, and metadata.
        """

        method = "POST"
        sub_url = "/entries/"
        query = {'query': {'entities': entities, 'text': text},
                 'limit': top_k}

        return self._make_request(sub_url, payload=query, method=method)


    def get_journals(self):
        """
        Get a list of all distinct journals in the db.

        Returns:
            List of distinct journal names
        """

        method = "GET"
        sub_url = "/stats/journals"
        return self._make_request(sub_url, method=method)

    def get_db_stats(self):
        """
         Get the statistics about the zumbi db.

        Returns:
            dictionary of stats. e.g
               {
                entities': 100
              }
        """

        method = "GET"
        sub_url = "/stats"

        return self._make_request(sub_url, method=method)


class ZumbiRestError(Exception):
    """
    Exception class for Rester.
    Raised when the query has problems, e.g., bad query format.
    """
    pass
