# -*- coding: utf-8 -*-
from pydebitoor.services.base import BaseService


class InvoiceService(BaseService):

    uri = '/sales/invoices'
    version = 'v1'
    validation_uri = '/sales/invoices/validate'

    def list(self, from_date=None, to_date=None):
        query_params = {}

        self._build_interval_params(query_params, from_date, to_date)
        return self.__list(**query_params)

    @classmethod
    def _build_interval_params(cls, query_params, from_date, to_date):
        if from_date:
            query_params['from_date'] = from_date
        if to_date:
            query_params['to_date'] = to_date
        if from_date and to_date and from_date > to_date:
            raise ValueError('Query interval is not coherent')

    @classmethod
    def _build_expand_params(cls, query_params, expand_customer, expand_product):
        expand = []
        if expand_customer:
            expand.append('customer')
        if expand_product:
            expand.append('product')
        if expand:
            query_params['expand'] = ','.join(expand)

    def get(self, invoice_id, expand_customer=False, expand_product=False):
        query_params = {}
        self._build_expand_params(query_params, expand_customer,
                                  expand_product)
        return self.__get(invoice_id, **query_params)

    def update(self, invoice_id, expand_customer=False, expand_product=False):
        query_params = {}
        self._build_expand_params(query_params, expand_customer,
                                  expand_product)
        return self.__get(invoice_id, **query_params)

    def copy(self, invoice_id):
        uri = '{}/{}/copy/v1'.format(self.uri, invoice_id, self.version)
        self.client.post(uri, payload={})

    def email(self, invoice_id):
        uri = '{}/{}/email/v2'.format(self.uri, invoice_id)
        self.client.post(uri, payload={})

    def pdf(self, invoice_id):
        uri = '{}/{}/pdf/'.format(self.uri, invoice_id, self.version)
        self.client.get(uri, payload={})

    def thumbnail(self, invoice_id):
        uri = '{}/{}/thumbnail/'.format(self.uri, invoice_id, self.version)
        self.client.get(uri, payload={})

    def headers(self, invoice_id=None, from_date=None, to_date=None):
        query_params = {}

        self._build_interval_params(query_params, from_date, to_date)
        if invoice_id:
            uri = '{}/headers/{}/{}'.format(self.uri, invoice_id, self.version)
        else:
            uri = '{}/headers/{}'.format(self.uri, self.version)

        return self.client.get(uri, **query_params)
