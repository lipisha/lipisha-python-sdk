import os
import datetime

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config

from formencode import Schema
from formencode import FancyValidator, Invalid
from formencode.validators import OneOf, Number, String
from pyramid_simpleform import Form


log = __import__('logging').getLogger('pyramid')


TYPE_INITIATE = 'Initiate'
TYPE_ACKNOWLEDGE = 'Acknowledge'
TYPE_RECEIPT = 'Receipt'
TYPE_PAYMENT = 'Payment'
TYPE_SETTLEMENT = 'Settlement'

LIPISHA_API_KEY = os.environ.get('lipisha_api_key')
LIPISHA_API_SIGNATURE = os.environ.get('lipisha_api_signature')
assert LIPISHA_API_KEY is not None, "LIPISHA_API_KEY environment variable must be defined"
assert LIPISHA_API_SIGNATURE is not None, "LIPISHA_API_SIGNATURE environment variable must be defined"
LIPISHA_API_VERSIONS = ['1.0.0', '1.0.4']
LIPISHA_API_TYPES = [TYPE_INITIATE, TYPE_ACKNOWLEDGE]
LIPISHA_TRANSACTION_TYPES = [TYPE_PAYMENT, TYPE_SETTLEMENT]

STATUS_SUCCESS = '001'
STATUS_ACKNOWLEDGED = '002'
STATUS_INITIATE_FAILURE = '002'
STATUS_INVALID_TRANSACTION = '003'
STATUS_ERROR_RECEIPT = '004'



class TimestampValidator(FancyValidator):
    """Validate timestamps
    """
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    messages = {
        'invalid': 'Invalid timestamp'
    }

    def to_python(self, value, state):
        try:
            return datetime.datetime.strptime(value, self.timestamp_format)
        except:
            msg = self.message('invalid', state)
            raise Invalid(msg, value, state)




class LipishaBaseSchema(Schema):
    allow_extra_fields = True
    transaction_reference = String(not_empty=True)

class LipishaInitiateSchema(LipishaBaseSchema):
    api_version = OneOf(LIPISHA_API_VERSIONS, not_empty=True)
    api_type = OneOf([TYPE_INITIATE], not_empty=True)
    transaction_date = TimestampValidator(not_empty=True)
    transaction_amount = Number(not_empty=True)
    transaction_type = OneOf(LIPISHA_TRANSACTION_TYPES, not_empty=True)
    transaction_method = String(not_empty=True)
    transaction_name = String(not_empty=True)
    transaction_mobile = String(not_empty=True)
    transaction_paybill = String(not_empty=True)
    transaction_account = String(not_empty=True)
    transaction_merchant_reference = String()

class LipishaAcknowledgeSchema(LipishaBaseSchema):
    api_type = OneOf([TYPE_ACKNOWLEDGE], not_empty=True)
    transaction_status_code = String(not_empty=True)
    transaction_status = String(not_empty=True)
    transaction_status_description = String(not_empty=True)

def process_lipisha_payment(request):
    """Handle payment received and respond with a dictionary"""
    log.debug(request.POST)
    schema = LipishaInitiateSchema
    api_type = request.POST.get('api_type')
    if api_type == TYPE_ACKNOWLEDGE:
        schema = LipishaAcknowledgeSchema
    form = Form(request, schema())
    transaction_status_code = STATUS_SUCCESS
    transaction_status = 'Processed'
    transaction_status_description = 'Processed'
    if form.validate():
        if api_type == TYPE_INITIATE:
            # Process new payment
            pass
        elif api_type == TYPE_ACKNOWLEDGE:
            if form.data.get('transaction_status_code') == STATUS_SUCCESS:
                # Process successful accknowledgement
                pass
            else:
                log.error('Invalid payment acknowledgement')
                log.error(request.POST)
    else:
        log.error("Error while processing payment")
        for error in form.all_errors():
            log.error(error)
        transaction_status_code = STATUS_INITIATE_FAILURE
        transaction_status = 'Error'
        transaction_status_description = 'Error while processing'
    if api_type == TYPE_INITIATE:
        data = request.POST
        return dict(
            api_key=LIPISHA_API_KEY,
            api_signature=LIPISHA_API_SIGNATURE,
            api_version=data.get('api_version'),
            api_type=TYPE_RECEIPT,
            transaction_reference=data.get('transaction_reference'),
            transaction_status_code=transaction_status_code,
            transaction_status=transaction_status,
            transaction_status_description=transaction_status_description,
        )
    return {}


class LipishadViews(object):
    """Payment views to receive callbacks from payment providers"""


    def __init__(self, request):
        self.request = request
        self.context = request.context

    @view_config(name='lipisha', renderer='json',
                 request_method='POST')
    def lipisha_ipn(self):
        """Process lipisha IPN - Initiate/Acknowledge"""
        if not (self.request.POST.get('api_key') == LIPISHA_API_KEY and
                self.request.POST.get('api_signature') == LIPISHA_API_SIGNATURE):
            raise HTTPBadRequest
        return process_lipisha_payment(self.request)

