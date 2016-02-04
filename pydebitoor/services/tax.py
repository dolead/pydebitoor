# -*- coding: utf-8 -*-
from pydebitoor.services.base import BaseService


class TaxService(BaseService):

    def purchase_tax_rates(self, supplier_country_code,
                           date, category_id=None):
        """
        Get applicable tax rates for purchase given a supplier country code and a date.
        Can give an optional category ID.
        Parameters
        ----------
        supplier_country_code: str
            Supplier country code
        date: str
            Date in 'YYYY-MM-DD' format
        category_id: str
            Category ID of the purchase.

        Returns
        -------
        Dict containing default tax rate
        and list of tax rates available for this supplier.

        ------
        Examples
            >>> TaxService().purchase_tax_rates('US', '2016-01-01')
            >>> {'baseTax': {'defaultRate': 0,
            >>>     'rates': [0]},
            >>>  'supplierCountry': 'US',
            >>>  'date': '2016-01-01',
            >>>  'reverseCharge': False,
            >>>  'mapFromCustomerCountry': 'US',
            >>>  'mapFromDate': '2016-01-01'}
        """
        query_params = {
            'supplierCountry': supplier_country_code,
            'date': date,
            'mapFromSupplierCountry': supplier_country_code,
            'mapFromDate': date
        }

        if category_id:
            query_params['categoryId'] = category_id
            query_params['mapFrompCategoryId'] = category_id


        return self.client.get('purchase/taxrates/v1', **query_params)



    def sale_tax_rates(self, customer_country_code, date):
        """
        Get tax rates applicable to a given customer at a given date.
        Parameters
        ----------
        customer_country_code: str
            Customer country code
        date: str
            Date in 'YYYY-MM-DD' format
        Returns
        -------
        Dict containing default tax rate
        and list of tax rates available for this customer.

        Examples
        --------
            >>> TaxService().sale_tax_rates('US', '2016-01-01')
            >>> {'baseTax': {'defaultRate': 0,
            >>>     'productServiceSplit': False,
            >>>     'rates': [0, 20, 10, 5.5]},
            >>>  'customerCountry': 'US',
            >>>  'date': '2016-01-01',
            >>>  'domesticToForeign': False,
            >>>  'domesticToIntraEu': False,
            >>>  'mapFromCustomerCountry': 'US',
            >>>  'mapFromDate': '2016-01-01'}
        """
        query_params = {
            'customerCountry': customer_country_code,
            'date': date,
            'mapFromCustomerCountry': customer_country_code,
            'mapFromDate': date
        }

        return self.client.get('/sales/taxrates/v1', **query_params)
