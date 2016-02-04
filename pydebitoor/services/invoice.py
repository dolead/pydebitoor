# -*- coding: utf-8 -*-
from pydebitoor.services.base import BaseService


class InvoiceService(BaseService):

    uri = '/sales/invoices'
    version = 'v1'
    validation_uri = '/sales/invoices/validate/v1'

    def list(self, from_date=None, to_date=None):
        query_params = {}

        self._build_interval_params(query_params, from_date, to_date)
        return self._list(**query_params)

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
        return self._get(invoice_id, **query_params)

    def update(self, invoice_id, expand_customer=False, expand_product=False):
        query_params = {}
        self._build_expand_params(query_params, expand_customer,
                                  expand_product)
        return self._get(invoice_id, **query_params)

    def copy(self, invoice_id):
        uri = '{}/{}/copy/v1'.format(self.uri, invoice_id, self.version)
        self.client.post(uri, payload={})

    def email(self, invoice_id, recipient, subject,
              cc_recipient=None, message=None, attachment_name=None,
              copy_mail=False, country_code=None):
        """
        Send invoice.

        Parameters
        ----------
        invoice_id: str
            ID of the draft invoice
        recipient: str
            Email of the recipient. Must be a valid email.
        subject: str
            Subject of the Email.
        cc_recipient: str or None
            If set, send the email throught CC to this recipient.
            Must be a valid email.
        message: str or None
            Email message. Optional
        attachment_name: str or None
            If set, invoice file will be named after this parameter.
        copy_mail: bool
            If true, send to yourself a BCC of this email.
        country_code: str or None
            Country code of the recipient.
            Must be a valid country code known by debitoor if specified.
            If not specified the current user country will be used.
        """
        payload = {
            'recipient': recipient,
            'subject': subject,
        }
        if cc_recipient:
            payload['ccRecipient'] = cc_recipient

        if message:
            payload['message'] = message

        if attachment_name:
            payload['attachmentName'] = attachment_name

        if copy_mail:
            payload['copyMail'] = copy_mail

        if country_code:
            payload['countryCode'] = country_code

        uri = '{}/{}/email/v2'.format(self.uri, invoice_id)
        return self.client.post(uri, payload=payload)

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
