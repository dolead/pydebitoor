# -*- coding: utf-8 -*-
from pydebitoor.services import InvoiceService


class DraftService(InvoiceService):
    """
    Draft service. Handle Draft Invoice management in Debitoor.
    Inherit from InvoiceService because all API methods are mirrored.
    """

    uri = '/sales/draftinvoices'
    version = 'v1'
    validation_uri = '/sales/draftinvoices/validate'

    def complete(self, draft_id, update_auto_number=False):
        """
        Complete a draft, an create a new invoice.
        Draft must be able to pass Invoice validation.
        If the invoice has no number, Debitoor will automatically generated
        it with the customerSettings.lastCustomerNumber

        Parameters
        ----------
        draft_id: str
            Id of the draft to complete
        update_auto_number: bool
            if true, will force invoice number to customerSettings.lastCustomerNumber

        Returns
        -------
            Dict representing the newly created invoice.

        """
        query_params = {}

        if update_auto_number:
            query_params = {'updateAutoNumber': 'true'}
        uri = '{}/{}/book/v1'.format(self.uri, self.version)
        self.client.post(uri, payload={}, **query_params)
