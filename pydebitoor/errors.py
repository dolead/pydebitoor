# -*- coding: utf-8 -*-
import pprint

from requests.exceptions import ConnectionError, HTTPError


class ApiConnectionError(ConnectionError):
    pass


class RequestError(HTTPError):
    def __init__(self, *args, **kwargs):
        super(RequestError, self).__init__(*args, **kwargs)
        if self.response:
            self.errors = self.response.json()['errors']
        else:
            self.errors = {}

    def __str__(self):
        return 'Invalid request: %s' % pprint.pformat(self.errors)


class NotFoundError(HTTPError):

    def __init__(self, *args, **kwargs):
        super(NotFoundError, self).__init__(*args, **kwargs)
        self.url = self.response.url

    def __str__(self):
        return 'API endpoint not found: %s' % self.url


class ApiError(HTTPError):
    pass
