# -*- coding: utf-8 -*-
import json
import logging

import requests
from requests.exceptions import ConnectionError, HTTPError

from .errors import RequestError, NotFoundError
from .services import (CustomerService, InvoiceService, DraftService,
                       TaxService)

logger = logging.getLogger('pydebitoor')
DEFAULT_API_URL = 'https://api.debitoor.com/api'
SERVICE_MAPPING = {
    'CustomerService': CustomerService,
    'DraftService': DraftService,
    'InvoiceService': InvoiceService,
    'TaxService': TaxService
}


class DebitoorClient(object):

    def __init__(self, access_token, base_url=None):
        self.access_token = access_token
        self.base_url = base_url or DEFAULT_API_URL
        self.__ensure_credentials()

    def __ensure_credentials(self):
        """
        Check if credentials are valid by performing a
        base query.

        Raises
        ------
        ConnectionError if credentials are invalid.

        """
        try:
            self.get('/environment/v1')
        except HTTPError as exc:
            logger.exception('Could not connect to the API')
            raise ConnectionError(exc)

    def __make_url(self, uri):
        """
        Build URL from URI.

        Parameters
        ----------
        uri: Ressource identifier

        Returns
        -------
            URL to query
        """
        return '{}{}'.format(self.base_url, uri)

    def __make_header(self):
        """
        Generate credential headers.

        Returns
        -------
            Dict reprensenting API header with credential.
        """
        return {'x-token': self.access_token,
                'Content-Type': 'application/json'}

    def __execute(self, method, url, **kwargs):
        """
        Execute API call.

        Parameters
        ----------
        method: str
            REST method, one of PUT, POST, PATCH, GET, DELETE
        args: list
            request call args.
        kwargs: dict
            request call kwargs

        Returns
        -------
        Call response, deserialized from Content-type
           If JSON, perform a json.loads transformation.
           Else, return response body as a string.

        Raises
        ------
        RequestError: If API call is invalid (Response code 400)
        NotFoundError: If url is  invalid (Response code 404)
        HTTPError: For any other error
        """
        headers = self.__make_header()
        headers.update(kwargs.pop('headers', {}))
        response = requests.request(method, url, headers=headers, **kwargs)
        if 200 <= response.status_code <= 299:
            if 'application/json' in response.headers['content-type']:
                return response.json()
            return response.content
        elif response.status_code == 400:
            logger.debug('Invalid request: %s', response.text)
            raise RequestError(response=response)
        elif response.status_code == 404:
            logger.debug('Invalid API endpoint: %s', url)
            raise NotFoundError(response=response)
        logger.debug('API Error [HTTP Code %s]: %s',
                     response.status_code, response.text)
        response.raise_for_status()

    def post(self, uri, payload, **params):
        """
        Parameters
        ----------
        uri: str
            URI of the resource (without API base url)
        payload: dict
            POST arguments.
        params: dict
            Querystring parameters
        Returns
        -------
            Call response as a dict

        Raises
        ------
        RequestError: If API call is invalid (Response code 400)
        NotFoundError: If url is  invalid (Response code 404)
        HTTPError: For any other error
        """
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        return self.__execute('POST', self.__make_url(uri),
                              data=payload, params=params)

    def get(self, uri, **params):
        """
        Perform a POST call to the debitoor API.

        Parameters
        ----------
        uri: str
            URI of the resource (without API base url)
        params: dict
            Querystring parameters
        Returns
        -------
            Call response as a dict

        Raises
        ------
        RequestError: If API call is invalid (Response code 400)
        NotFoundError: If url is  invalid (Response code 404)
        HTTPError: For any other error
        """
        return self.__execute('GET', self.__make_url(uri), params=params)

    def put(self, uri, payload, **params):
        """
        Perform a PUT call to the debitoor API.

        Parameters
        ----------
        uri: str
            URI of the resource (without API base url)
        payload: dict
            POST arguments.
        params: dict
            Querystring parameters
        Returns
        -------
            Call response as a dict

        Raises
        ------
        RequestError: If API call is invalid (Response code 400)
        NotFoundError: If url is  invalid (Response code 404)
        HTTPError: For any other error
        """
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        return self.__execute('PUT', self.__make_url(uri), data=payload,
                              params=params)

    def delete(self, uri, **params):
        """
        Perform a DELETE call to the debitoor API.

        Parameters
        ----------
        uri: str
            URI of the resource (without API base url)
        params: dict
            Querystring parameters
        Returns
        -------
            Call response as a dict

        Raises
        ------
        RequestError: If API call is invalid (Response code 400)
        NotFoundError: If url is  invalid (Response code 404)
        HTTPError: For any other error
        """
        return self.__execute('DELETE', self.__make_url(uri), params=params)

    def patch(self, uri, payload, **params):
        """
        Perform a PATCH call to the debitoor API.

        Parameters
        ----------
        uri: str
            URI of the resource (without API base url)
        payload: dict
            POST arguments.
        params: dict
            Querystring parameters
        Returns
        -------
            Call response as a dict

        Raises
        ------
        RequestError: If API call is invalid (Response code 400)
        NotFoundError: If url is  invalid (Response code 404)
        HTTPError: For any other error
        """
        return self.__execute('PATCH', self.__make_url(uri),
                              data=payload, params=params)

    def get_service(self, service_name):
        """
        Get Debitoor service form name.

        Parameters
        ----------
        service_name:
            Name of service. Must be one of CustomerService,
            DraftService, InvoiceService.

        Returns
        -------
            Service instance.

        Raises
        -------
            Value Error if the service does not exist
        """
        try:
            return SERVICE_MAPPING[service_name](self)
        except KeyError:
            raise ValueError('Unknown service: %s' % service_name)
