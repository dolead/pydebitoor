***********************************
PyDebitoor: Connect to Debitoor API
***********************************

PyDebitoor is a library to access to basic Debitoor_ operation resources through its REST API.
Currently, it only can manage customers, invoices and draft.

.. _Debitoor : https://debitoor.com

.. code-block:: python

    from pydebitoor.client import DebitoorClient

    client = DebitoorClient('access_token')
    service = client.get_service('CustomerService')

    service.list()  # Getting all customers
    >>> [{'address': 'Customer1 Address',
          'countryCode': 'FR',
          'email': 'Customer1 Email',
          'id': 'Customer1 Debitoor ID',
          'name': 'Customer1 Name',
          'number': 1,
          'paymentTermsId': 1},
         {'countryCode': 'FR',
          'id': 'Customer2 Debitoor ID',
          'name': 'Customer2 Name',
          'number': 2,
          'paymentTermsId': 3
         }]

SUPPORTED SERVICES:
 - CustomerService
 - DraftService
 - InvoiseService

TODO:
 - Support all services (product, expenses, quotes, incomes, etc.)
 - Better Error management
 - Testing (need a sandbox environment)
 - Better commentaries and examples