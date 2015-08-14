=====
Usage
=====

Install Lipisha

    pip install lipisha

Sample usage session
====================

.. code-block:: python

    >>> from lipisha import Lipisha
    >>> api_key = "YOUR API KEY"    
    >>> api_signature = "YOUR API SIGNATURE"
    >>> lipisha = Lipisha(api_key, api_signature)
    >>> lipisha.api_base_url
    'https://lipisha.com/payments/accounts/index.php/v2/api'
    >>> lipisha = Lipisha(api_key, api_signature, api_environment='test')
    >>> lipisha.api_base_url
    'http://developer.lipisha.com/index.php/v2/api/'
    >>> lipisha = Lipisha(api_key, api_signature, api_environment='live')
    >>> lipisha.api_base_url
    'https://lipisha.com/payments/accounts/index.php/v2/api'

    >>> lipisha.confirm_transaction(transaction='YYYE9WWWW0')
    
    {u'content': {u'transaction': u'YYYE9WWWW0',
      u'transaction_account_name': u'Primary',
      u'transaction_account_number': u'098777',
      u'transaction_amount': u'200.0000',
      u'transaction_date': u'2015-08-14 16:51:00',
      u'transaction_email': u'',
      u'transaction_method': u'Paybill (M-Pesa)',
      u'transaction_mobile_number': u'2547XXYYYZZZ',
      u'transaction_name': u'Test User Names',
      u'transaction_reference': u'99',
      u'transaction_status': u'Completed',
      u'transaction_type': u'Payment'},
      u'status': {u'status': u'SUCCESS',
                  u'status_code': 0,
                  u'status_description': u'Transaction Found'}}


    >>> lipisha.create_payment_account(transaction_account_type=1,
                                       transaction_account_name="MPESA Payments",
                                       transaction_account_manager="test_account")
    
    {u'content': {u'transaction_account_manager': u'test_account',
      u'transaction_account_name': u'MPESA Payments',
      u'transaction_account_number': u'09999',
      u'transaction_account_type': u'1'},
      u'status': {u'status': u'SUCCESS',
                  u'status_code': 0,
                  u'status_description': u'Account Created'}}

    >>> lipisha.create_withdrawal_account(transaction_account_type="1",
                                   transaction_account_name="Settlement Bank A/C",
                                   transaction_account_number="0100555555555",
                                   transaction_account_bank_name="AZY Bank",
                                   transaction_account_bank_branch="HQ",
                                   transaction_account_bank_address="PO BOX 900032 - 99999 Nairobi, Kenya",
                                   transaction_account_swift_code="ABCXYXXXX",
                                   transaction_account_manager="test_account")
    {u'content': {u'transaction_account_bank_address': u'PO BOX 900032 - 99999 Nairobi, Kenya',
      u'transaction_account_bank_branch': u'HQ',
      u'transaction_account_bank_name': u'AZY Bank',
      u'transaction_account_manager': u'test_account',
      u'transaction_account_name': u'Settlement Bank A/C',
      u'transaction_account_number': u'0100555555555',
      u'transaction_account_swift_code': u'ABCXYXXXX',
      u'transaction_account_type': u'1'},
      u'status': {u'status': u'SUCCESS',
                  u'status_code': 0,
                  u'status_description': u'Account Created'}}

    >>> lipisha.get_balance()
    {u'content': {u'balance': u'246.2500', u'currency': u'KES'},
     u'status': {u'status': u'SUCCESS',
                 u'status_code': 0,
                 u'status_description': u'Balance Found'}}

    >>> lipisha.get_float(account_number="098000")
    
    {u'content': {u'account_number': u'098000',
      u'currency': u'KES',
      u'float': u'0.00'},
     u'status': {u'status': u'SUCCESS',
      u'status_code': 0,
      u'status_description': u'Float Found'}}

    >>> lipisha.get_transactions()
    
    {u'content': [{u'code': None,
       u'transaction': u'JJ99X9TC0',
       u'transaction_account_name': u'Primary',
       u'transaction_account_number': u'098777',
       u'transaction_amount': u'50.0000',
       u'transaction_date': u'2015-08-06 10:39:00',
       u'transaction_email': u'',
       u'transaction_method': u'Paybill (M-Pesa)',
       u'transaction_mobile_number': u'2547XXYYYZZZ',
       u'transaction_name': u'Test User Names',
       u'transaction_reference': u'',
       u'transaction_reversal_status': u'None',
       u'transaction_reversal_status_id': u'1',
       u'transaction_status': u'Completed',
       u'transaction_type': u'Payment'},
      {u'code': None,
       u'transaction': u'JJ99X9TC0',
       u'transaction_account_name': u'Primary',
       u'transaction_account_number': u'098777',
       u'transaction_amount': u'-0.7500',
       u'transaction_date': u'2015-08-06 10:39:00',
       u'transaction_email': u'',
       u'transaction_method': u'Paybill (M-Pesa)',
       u'transaction_mobile_number': u'2547XXYYYZZZ',
       u'transaction_name': u'Test User Names',
       u'transaction_reference': u'',
       u'transaction_reversal_status': u'None',
       u'transaction_reversal_status_id': u'1',
       u'transaction_status': u'Completed',
       u'transaction_type': u'Fee'},
      {u'code': None,
       u'transaction': u'YYYE9WWWW0',
       u'transaction_account_name': u'Primary',
       u'transaction_account_number': u'098777',
       u'transaction_amount': u'200.0000',
       u'transaction_date': u'2015-08-14 16:51:00',
       u'transaction_email': u'',
       u'transaction_method': u'Paybill (M-Pesa)',
       u'transaction_mobile_number': u'2547XXYYYZZZ',
       u'transaction_name': u'Test User Names',
       u'transaction_reference': u'99',
       u'transaction_reversal_status': u'None',
       u'transaction_reversal_status_id': u'1',
       u'transaction_status': u'Completed',
       u'transaction_type': u'Payment'},
      {u'code': None,
       u'transaction': u'YYYE9WWWW0',
       u'transaction_account_name': u'Primary',
       u'transaction_account_number': u'098777',
       u'transaction_amount': u'-3.0000',
       u'transaction_date': u'2015-08-14 16:51:00',
       u'transaction_email': u'',
       u'transaction_method': u'Paybill (M-Pesa)',
       u'transaction_mobile_number': u'2547XXYYYZZZ',
       u'transaction_name': u'Test User Names',
       u'transaction_reference': u'99',
       u'transaction_reversal_status': u'None',
       u'transaction_reversal_status_id': u'1',
       u'transaction_status': u'Completed',
       u'transaction_type': u'Fee'}],
     u'status': {u'status': u'SUCCESS',
      u'status_code': 0,
      u'status_description': u'Transactions Found'}}

    >>> lipisha.get_transactions(transaction="JJ99X9TC0")
    {u'content': [{u'code': None,
       u'transaction': u'JJ99X9TC0',
       u'transaction_account_name': u'Primary',
       u'transaction_account_number': u'098777',
       u'transaction_amount': u'50.0000',
       u'transaction_date': u'2015-08-06 10:39:00',
       u'transaction_email': u'',
       u'transaction_method': u'Paybill (M-Pesa)',
       u'transaction_mobile_number': u'2547XXYYYZZZ',
       u'transaction_name': u'Test User Names',
       u'transaction_reference': u'',
       u'transaction_reversal_status': u'None',
       u'transaction_reversal_status_id': u'1',
       u'transaction_status': u'Completed',
       u'transaction_type': u'Payment'},
      {u'code': None,
       u'transaction': u'JJ99X9TC0',
       u'transaction_account_name': u'Primary',
       u'transaction_account_number': u'098777',
       u'transaction_amount': u'-0.7500',
       u'transaction_date': u'2015-08-06 10:39:00',
       u'transaction_email': u'',
       u'transaction_method': u'Paybill (M-Pesa)',
       u'transaction_mobile_number': u'2547XXYYYZZZ',
       u'transaction_name': u'Test User Names',
       u'transaction_reference': u'',
       u'transaction_reversal_status': u'None',
       u'transaction_reversal_status_id': u'1',
       u'transaction_status': u'Completed',
       u'transaction_type': u'Fee'}],
     u'status': {u'status': u'SUCCESS',
      u'status_code': 0,
      u'status_description': u'Transactions Found'}}

    >>> lipisha.get_customers()
    {u'content': [{u'customer_average': u'125.00000000',
       u'customer_email': u'',
       u'customer_first_payment_date': u'2015-08-06 10:39:00',
       u'customer_last_payment_date': u'2015-08-14 16:51:00',
       u'customer_mobile_number': u'2547XXYYYZZZ',
       u'customer_name': u'Test User Names',
       u'customer_payments': u'2',
       u'customer_total': u'250.0000'}],
     u'status': {u'status': u'SUCCESS',
      u'status_code': 0,
      u'status_description': u'Customers Found'}}

    >>> lipisha.get_customers(customer_mobile_number="2547XXYYYZZZ")
    {u'content': [{u'customer_average': u'125.00000000',
       u'customer_email': u'',
       u'customer_first_payment_date': u'2015-08-06 10:39:00',
       u'customer_last_payment_date': u'2015-08-14 16:51:00',
       u'customer_mobile_number': u'2547XXYYYZZZ',
       u'customer_name': u'Test User Names',
       u'customer_payments': u'2',
       u'customer_total': u'250.0000'}],
     u'status': {u'status': u'SUCCESS',
      u'status_code': 0,
      u'status_description': u'Customers Found'}}

    >>> lipisha.send_airtime(account_number="03160", mobile_number="07XXYYYZZZ", amount="50", network="SAF")
    {u'content': {u'amount': u'50',
      u'mobile_number': u'07XXYYYZZZ',
      u'reference': u'MF0QKVD9W'},
     u'status': {u'status': u'SUCCESS',
      u'status_code': u'0000',
      u'status_description': u'Airtime purchased successfully'}}



    >>> fortress.send_money(account_number="00396", mobile_number="07XXYYYZZZ", amount=50)
    {u'content': {u'amount': u'50',
      u'customer_name': u'',
      u'mobile_number': u'07XXYYYZZZ',
      u'reference': u'SP01ZXA45'},
     u'status': {u'status': u'SUCCESS',
      u'status_code': u'0000',
      u'status_description': u'Payout Scheduled'}}


    >>> lipisha.authorize_card_transaction(account_number="098000",
                                           card_number="4242424242424242",
                                           address1="PO BOX 11111 99999",
                                           address2="",
                                           expiry="082020",
                                           name="Lipsha Test Account",
                                           country="KENYA",
                                           state="NAIROBI",
                                           zip="00200",
                                           security_code="999",
                                           amount=100,
                                           currency='KES')
    {u'content': {u'transaction_index': u'{CDD55BEB-F74A-4A8B-8D5C-2FC77FF14E7B}',
      u'transaction_reference': 111111},
     u'status': {u'status': u'SUCCESS',
      u'status_code': u'0000',
      u'status_description': u'Transaction Authorized Successfully'}}


    >>> lipisha.complete_card_transaction(transaction_reference=11111,
                                          transaction_index="{CDD55BEB-F74A-4A8B-8D5C-2FC77FF14E7B}")    
    {u'content': {u'transaction_index': u'{CDD55BEB-F74A-4A8B-8D5C-2FC77FF14E7B}',
      u'transaction_reference': u'11111'},
     u'status': {u'status': u'SUCCESS',
      u'status_code': u'0000',
      u'status_description': u'Transaction Completed Successfully'}}

    >>> lipisha.reverse_card_transaction(transaction_reference=11111, transaction_index="{CDD55BEB-F74A-4A8B-8D5C-2FC77FF14E7B}")
    {u'content': None, u'status': None}


======================
Full API Documentation
======================

See :doc:`Full API Documentation </lipisha>` 
