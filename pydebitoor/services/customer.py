# -*- coding: utf-8 -*-
from pydebitoor.services.base import BaseService


class CustomerService(BaseService):

    uri = '/customers'
    version = 'v1'
    validation_uri = '/sales/customers/validate/v1'
    allow_partial_update = True

    def create(self, customer, auto_number=False):
        """
        Create a new customer in Debitoor
        Parameters
        ----------
        element: dict
            describe

        Returns
        -------
        Customer

        Raises
        ------
        `pydebitoor.exceptions.InvalidRequest`:
        """
        query_params = {}
        if auto_number:
            query_params = {'autonumber': 'true'}
        return self.__create(customer, **query_params)

    def update(self, customer_id, customer, auto_number=False):
        """
        Create a new customer in Debitoor
        Parameters
        ----------
        element: dict
            describe

        Returns
        -------

        """
        query_params = {}
        if auto_number:
            query_params = {'autonumber': 'true'}
        return self.__update(customer_id, customer, **query_params)
