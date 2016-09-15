#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_lipisha
----------------------------------

Tests for `lipisha` module.
'''

import sys
import os
import logging
import unittest

from lipisha import Lipisha

TEST_ENVIRONMENT = os.environ.get('LIPISHA_TEST_ENVIRONMENT', 'test')
API_KEY = os.environ.get('LIPISHA_TEST_API_KEY')
API_SIGNATURE = os.environ.get('LIPISHA_TEST_API_SIGNATURE')
TEST_MOBILE_NUMBER = os.environ.get('LIPISHA_TEST_MOBILE_NUMBER')
TEST_PAYOUT_ACCOUNT = os.environ.get('LIPISHA_TEST_PAYOUT_ACCOUNT')
TEST_PAYOUT_AMOUNT = os.environ.get('LIPISHA_TEST_PAYOUT_AMOUNT')
TEST_TRANSACTION_ID = os.environ.get('LIPISHA_TEST_TRANSACTION_ID')

assert API_KEY is not None, ('You need to set up test environment: '
                             ' export LIPISHA_TEST_API_KEY=<your_api_key>')
assert API_SIGNATURE is not None, ('You need to set up test environnment: '
                                   'export LIPISHA_TEST_API_SIGNATURE='
                                   '<your_api_signature>')


def setUpModule():
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger().setLevel(logging.DEBUG)


def make_client():
    return Lipisha(API_KEY, API_SIGNATURE, api_environment=TEST_ENVIRONMENT)


class BaseTest(unittest.TestCase):
    api_method = ''
    required_parameters = []
    parameter_mapping = []
    default_parameters = {}
    response_tests = []

    def runTest(self):
        if not self.api_method:
            return
        assert len(self.required_parameters) == len(self.parameter_mapping), \
            "Check Parameter Setup for this Test"
        param_values = [os.environ.get(p) for p in self.required_parameters]
        missing_params = [self.required_parameters[i]
                          for i, v in enumerate(param_values) if v is None]
        if missing_params:
            env = ', '.join(missing_params)
            logging.debug('%s:Skipped: You must define environment vars: %s',
                          self.__class__.__name__, env)
            return
        client = make_client()
        params = dict(zip(self.parameter_mapping, param_values))
        params.update(self.default_parameters)
        logging.debug('Calling: %s with params: %r', self.api_method, params)
        response = getattr(client, self.api_method)(**params)
        self.assertIsInstance(response, dict)
        for t in self.response_tests:
            self.assertTrue(t(response), 'Test failed')
        logging.debug('%s response: %r', self.api_method, response)


class TestLipishaGetBalance(BaseTest):

    api_method = 'get_balance'


class TestLipishaGetFloat(BaseTest):

    api_method = 'get_float'
    required_parameters = ['LIPISHA_TEST_PAYOUT_ACCOUNT']
    parameter_mapping = ['account_number']


class TestLipishaSendMoney(BaseTest):

    api_method = 'send_money'
    required_parameters = ['LIPISHA_TEST_MOBILE_NUMBER',
                           'LIPISHA_TEST_PAYOUT_ACCOUNT',
                           'LIPISHA_TEST_PAYOUT_AMOUNT']
    parameter_mapping = ['mobile_number', 'account_number', 'amount']


class TestLipishaRequestMoney(BaseTest):

    api_method = 'request_money'
    default_parameters = dict(method='Paybill (M-Pesa)',
                              currency='KES',
                              reference='TEST-REFERENCE')
    required_parameters = ['LIPISHA_TEST_MOBILE_NUMBER',
                           'LIPISHA_TEST_REQUEST_ACCOUNT',
                           'LIPISHA_TEST_REQUEST_AMOUNT']
    parameter_mapping = ['mobile_number', 'account_number', 'amount']

class TestLipishaAcknowledgeTransaction(BaseTest):

    api_method = 'acknowledge_transaction'
    required_parameters = ['LIPISHA_TEST_TRANSACTION_ID']
    parameter_mapping = ['transaction']


class TestLipishaConfirmTransaction(TestLipishaAcknowledgeTransaction):

    api_method = 'confirm_transaction'


class TestLipishaReverseTransaction(TestLipishaAcknowledgeTransaction):

    api_method = 'reverse_transaction'


class TestLipishaSendAirtime(BaseTest):

    api_method = 'send_airtime'
    required_parameters = ['LIPISHA_TEST_AIRTIME_ACCOUNT',
                           'LIPISHA_TEST_MOBILE_NUMBER',
                           'LIPISHA_TEST_AIRTIME_AMOUNT',
                           'LIPISHA_TEST_MOBILE_NETWORK']
    parameter_mapping = [
        'account_number',
        'mobile_number',
        'amount',
        'network']


class TestLipishaSendSMS(BaseTest):

    api_method = 'send_sms'
    required_parameters = [
        'LIPISHA_TEST_MOBILE_NUMBER',
        'LIPISHA_TEST_SMS_MESSAGE']
    parameter_mapping = ['mobile_number', 'message']


class TestLipishaCreateUser(BaseTest):

    api_method = 'create_user'
    required_parameters = ['LIPISHA_TEST_USER_FULL_NAME',
                           'LIPISHA_TEST_USER_ROLE',
                           'LIPISHA_TEST_USER_MOBILE_NUMBER',
                           'LIPISHA_TEST_USER_EMAIL',
                           'LIPISHA_TEST_USER_LOGIN',
                           'LIPISHA_TEST_USER_PASSWORD']
    parameter_mapping = ['full_name', 'role', 'mobile_number', 'email',
                         'user_name', 'password']


class TestLipishaCreatePaymentAccount(BaseTest):

    api_method = 'create_payment_account'
    required_parameters = ['LIPISHA_TEST_PAYMENT_ACCOUNT_TYPE',
                           'LIPISHA_TEST_PAYMENT_ACCOUNT_NAME',
                           'LIPISHA_TEST_PAYMENT_ACCOUNT_MANAGER']
    parameter_mapping = [
        'transaction_account_type',
        'transaction_account_name',
        'transaction_account_manager']


class TestLipishaCreateWithdrawalAccount(BaseTest):

    api_method = 'create_withdrawal_account'
    required_parameters = ['LIPISHA_TEST_WITHDRAWAL_ACCOUNT_TYPE',
                           'LIPISHA_TEST_WITHDRAWAL_ACCOUNT_NAME',
                           'LIPISHA_TEST_WITHDRAWAL_ACCOUNT_NUMBER',
                           'LIPISHA_TEST_WITHDRAWAL_ACCOUNT_BANK_NAME',
                           'LIPISHA_TEST_WITHDRAWAL_ACCOUNT_BANK_BRANCH',
                           'LIPISHA_TEST_WITHDRAWAL_ACCOUNT_BANK_ADDRESS',
                           'LIPISHA_TEST_WITHDRAWAL_ACCOUNT_BANK_SWIFT_CODE',
                           'LIPISHA_TEST_WITHDRAWAL_ACCOUNT_MANAGER']
    parameter_mapping = ['transaction_account_type',
                         'transaction_account_name',
                         'transaction_account_number',
                         'transaction_account_bank_name',
                         'transaction_account_bank_branch',
                         'transaction_account_bank_address',
                         'transaction_account_swift_code',
                         'transaction_account_manager', ]


class TestLipishaGetTransactions(BaseTest):

    api_method = 'get_transactions'


class TestLipishaGetTransactionsOffset(BaseTest):

    api_method = 'get_transactions'
    default_parameters = dict(offset=0, limit=1)
    response_tests = [(lambda r: len(r['content']) in [0, 1])]


class TestLipishaGetTransactionsFilterTransaction(BaseTest):

    api_method = 'get_transactions'
    required_parameters = ['LIPISHA_TEST_TRANSACTIONS_TRANSACTION_ID']
    parameter_mapping = ['transaction']


class TestLipishaGetCustomers(BaseTest):

    api_method = 'get_customers'


class TestLipishaGetCustomersFiltered(BaseTest):

    api_method = 'get_customers'
    required_parameters = ['LIPISHA_TEST_CUSTOMERS_MOBILE_NUMBER']
    parameter_mapping = ['customer_mobile_number']


class TestLipishaAuthorizeCardTransaction(BaseTest):

    api_method = 'authorize_card_transaction'
    required_parameters = ['LIPISHA_TEST_CARD_AUTH_ACCOUNT_NUMBER',
                           'LIPISHA_TEST_CARD_AUTH_CARD_NUMBER',
                           'LIPISHA_TEST_CARD_AUTH_ADDRESS1',
                           'LIPISHA_TEST_CARD_AUTH_ADDRESS2',
                           'LIPISHA_TEST_CARD_AUTH_EXPIRY',
                           'LIPISHA_TEST_CARD_AUTH_NAME',
                           'LIPISHA_TEST_CARD_AUTH_COUNTRY',
                           'LIPISHA_TEST_CARD_AUTH_STATE',
                           'LIPISHA_TEST_CARD_AUTH_ZIP',
                           'LIPISHA_TEST_CARD_AUTH_SECURITY_CODE',
                           'LIPISHA_TEST_CARD_AUTH_AMOUNT',
                           'LIPISHA_TEST_CARD_AUTH_CURRENCY']
    parameter_mapping = ['account_number',
                         'card_number',
                         'address1',
                         'address2',
                         'expiry',
                         'name',
                         'country',
                         'state',
                         'zip',
                         'security_code',
                         'amount',
                         'currency']


class TestLipishaReverseCardTransaction(BaseTest):

    api_method = 'reverse_card_transaction'
    required_parameters = ['LIPISHA_TEST_CARD_REVERSE_TRANSACTION_INDEX',
                           'LIPISHA_TEST_CARD_REVERSE_TRANSACTION_REFERENCE']
    parameter_mapping = ['transaction_index', 'transaction_reference']


class TestLipishaCompleteCardTransaction(BaseTest):

    api_method = 'reverse_card_transaction'
    required_parameters = ['LIPISHA_TEST_CARD_COMPLETE_TRANSACTION_INDEX',
                           'LIPISHA_TEST_CARD_COMPLETE_TRANSACTION_REFERENCE']
    parameter_mapping = ['transaction_index', 'transaction_reference']


class TestLipishaVoidCardTransaction(BaseTest):

    api_method = 'void_card_transaction'
    required_parameters = ['LIPISHA_TEST_CARD_VOID_TRANSACTION_INDEX',
                           'LIPISHA_TEST_CARD_VOID_TRANSACTION_REFERENCE']
    parameter_mapping = ['transaction_index', 'transaction_reference']
