# -*- coding: utf-8 -*-

# Configuration
DEFAULT_API_VERSION = '1.3.0'
API_BASE_URL = 'https://lipisha.com/payments/accounts/index.php/v2/api'
API_SANDBOX_URL = 'http://developer.lipisha.com/index.php/v2/api/'

# API Configuration: (<method_name> , <expected_parameters>,
# <optional_parameters>)

DEFAULT_OPTIONAL_PARAMETERS = ['api_version', 'api_type']

API_METHOD_CONFIGURATION = (
    ('get_balance', ['api_type'], []),
    ('send_money', ['account_number', 'mobile_number', 'amount'], []),
    ('get_float', ['account_number'], []),
    ('send_sms', ['mobile_number', 'message'], []),
    ('acknowledge_transaction', ['transaction'], []),
    ('confirm_transaction', ['transaction'], []),
    ('reverse_transaction', ['transaction'], []),
    ('send_airtime', [
     'account_number', 'mobile_number', 'amount', 'network'], []),
    ('create_user', ['full_name', 'role', 'mobile_number',
                     'email', 'user_name', 'password'], []),
    ('update_user', [
     'full_name', 'role', 'mobile_number', 'email', 'user_name'], []),
    ('create_payment_account', ['transaction_account_type',
                                'transaction_account_name',
                                'transaction_account_manager'],
     []),
    ('create_withdrawal_account', ['transaction_account_type',
                                   'transaction_account_name',
                                   'transaction_account_number',
                                   'transaction_account_bank_name',
                                   'transaction_account_bank_branch',
                                   'transaction_account_bank_address',
                                   'transaction_account_swift_code',
                                   'transaction_account_manager', ],
     []),
    ('get_transactions', [], ['transaction',
                              'transaction_type',
                              'transaction_method',
                              'transaction_date_start',
                              'transaction_date_end',
                              'transaction_account_name',
                              'transaction_account_number',
                              'transaction_reference',
                              'transaction_amount_minimum',
                              'transaction_amount_maximum',
                              'transaction_status',
                              'transaction_name',
                              'transaction_mobile_number',
                              'transaction_email',
                              'limit',
                              'offset']),
    ('get_customers', [], ['customer_name',
                           'customer_mobile_number',
                           'customer_email',
                           'customer_first_payment_from',
                           'customer_first_payment_to',
                           'customer_last_payment_from',
                           'customer_last_payment_to',
                           'customer_payments_minimum',
                           'customer_payments_maximum',
                           'customer_total_spent_minimum',
                           'customer_total_spent_maximum',
                           'customer_average_spent_minimum',
                           'customer_average_spent_maximum',
                           'limit',
                           'offset']),
    ('authorize_card_transaction', ['account_number',
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
                                    'currency'],
     []),
    ('reverse_card_transaction', [
     'transaction_index', 'transaction_reference'], []),
    ('complete_card_transaction', [
     'transaction_index', 'transaction_reference'], []),
    ('void_card_transaction', [
     'transaction_index', 'transaction_reference'], []),
    ('request_settlement', ['account_number', 'amount'], []),
)

PARAMETER_DEFAULTS = {
    'api_type': 'Callback',
    'limit': 1000,
    'offset': 0
}
