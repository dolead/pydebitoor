***********************************
PyDebitoor: Connect to Debitoor API
***********************************

PyDebitoor is a library to access to basic Debitoor operation resources through its REST API.

.. code-block:: python

    from pydebitoor.client import DebitoorClient

    client = DebitoorClient('access_token')
    service = client.get_service('CustomerService')

    service.list()  # Getting all customers
    >>> []

    client.get_campaigns(1951282421)  # Getting campaign with Id 1951282421
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
