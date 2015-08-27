import os

from django import forms

LIPISHA_API_KEY = os.environ.get('LIPISHA_API_KEY')
LIPISHA_API_SIGNATURE = os.environ.get('LIPISHA_API_SIGNATURE')

assert LIPISHA_API_KEY is not None, 'LIPISHA_API_KEY must be defined'
assert LIPISHA_API_SIGNATURE is not None, 'LIPISHA_API_SIGNATURE must be defined'

TYPE_INITIATE = 'Initiate'
TYPE_ACKNOWLEDGE = 'Acknowledge'
TYPE_RECEIPT = 'Receipt'
TYPE_PAYMENT = 'Payment'
TYPE_SETTLEMENT = 'Settlement'

LIPISHA_API_VERSIONS = ['1.0.0', '1.0.4']
LIPISHA_API_TYPES = [TYPE_INITIATE, TYPE_ACKNOWLEDGE]
LIPISHA_TRANSACTION_TYPES = [TYPE_PAYMENT, TYPE_SETTLEMENT]

STATUS_SUCCESS = '001'
STATUS_ACKNOWLEDGED = '002'
STATUS_INITIATE_FAILURE = '002'
STATUS_INVALID_TRANSACTION = '003'
STATUS_ERROR_RECEIPT = '004'


LOG = __import__('logging').getLogger('django')

def make_choices(choice_list):
    return [(v, v) for v in choice_list]

class LipishaInitiateForm(forms.Form):
    api_version = forms.ChoiceField(choices=make_choices(LIPISHA_API_VERSIONS))
    api_type = forms.ChoiceField(choices=make_choices([TYPE_INITIATE]))
    transaction_reference = forms.CharField()
    transaction_date = forms.DateTimeField()
    transaction_amount = forms.DecimalField()
    transaction_type = forms.ChoiceField(choices=make_choices(LIPISHA_TRANSACTION_TYPES))
    transaction_method = forms.CharField()
    transaction_name = forms.CharField()
    transaction_mobile = forms.CharField()
    transaction_paybill = forms.CharField()
    transaction_account = forms.CharField()
    transaction_merchant_reference = forms.CharField()

    def process_payment(self):
        """
         Processs payment data here.
        """
        payment_data = self.cleaned_data
        LOG.debug("Received Payment Data: %r", payment_data)
        # Implement processing of payment data here


class LipishaAcknowledgeForm(forms.Form):
    transaction_reference = forms.CharField()
    api_type = forms.ChoiceField(choices=make_choices([TYPE_ACKNOWLEDGE]))
    transaction_status_code = forms.CharField()
    transaction_status = forms.CharField()
    transaction_status_description = forms.CharField()

    def process_payment(self):
        payment_data = self.cleaned_data
        LOG.debug("Received Payment Data: %r", payment_data)
        # Implement processing of payment data here
