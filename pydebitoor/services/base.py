# -*- coding: utf-8 -*-


class BaseService(object):
    uri = None
    version = None
    validation_uri = None
    allow_partial_update = False

    def __init__(self, client):
        self.client = client

    def __make_uri(self, uri=None, element_id=None):
        assert self.uri is not None and self.version is not None, \
            'Service does not have a specific URI set. ' \
            'CRUD operation are disabled'
        if uri:
            return '{}/{}'.format(uri, self.version)
        elif element_id:
            return '{}/{}/{}'.format(self.uri, element_id, self.version)
        return '{}/{}'.format(self.uri, self.version)

    def validate(self, payload, validation_uri=None):
        """
        Validate the payload of a create action.

        Parameters
        ----------
        payload: dict
            Entity to validate
        Returns
        -------

        Raises
        ------
        ValueError if payload is not valid.

        """
        validation_uri = validation_uri or self.validation_uri
        if not validation_uri:
            return True

        response = self.client.post(validation_uri, payload=payload)
        if response.status_code == 200:
            return True
        try:
            return ValueError(response.json()['errors'])
        except:
            response.raise_for_status()

    def list(self):
        return self._list()


    def create(self, element):
        return self._create(element)

    def get(self, element_id):
        return self._get(element_id)

    def delete(self, element_id):
        return self._delete(element_id)

    def update(self, element_id, payload):
        return self._update(element_id, payload)

    def partial_update(self, element_id, payload):
        return self._partial_update(element_id, payload)

    def _create(self, element, **query_params):
        """
        Abstract element creator

        Parameters
        ----------
        element: dict
            Element to create as a dict

        Returns
        -------

        """
        self.validate(element)
        return self.client.post(self.__make_uri(), payload=element, **query_params)

    def _list(self, **query_params):
        return self.client.get(self.__make_uri(), **query_params)

    def _get(self, element_id, **query_params):
        return self.client.get(self.__make_uri(element_id=element_id), **query_params)

    def _delete(self, element_id, **query_params):
        return self.client.delete(self.__make_uri(element_id=element_id), **query_params)

    def _update(self, element_id, payload, **query_params):
        return self.client.put(self.__make_uri(element_id=element_id), payload, **query_params)

    def _partial_update(self, element_id, payload, **query_params):
        if not self.allow_partial_update:
            raise ValueError('%s does not support partial update' % self.__class__.__name__)
        return self.client.patch(self.__make_uri(element_id=element_id), payload, **query_params)
