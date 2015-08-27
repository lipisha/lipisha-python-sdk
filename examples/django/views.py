from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.views.generic import View

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .forms import LIPISHA_API_KEY
from .forms import LIPISHA_API_SIGNATURE
from .forms import TYPE_ACKNOWLEDGE
from .forms import TYPE_INITIATE
from .forms import TYPE_RECEIPT
from .forms import STATUS_SUCCESS
from .forms import STATUS_INITIATE_FAILURE
from .forms import LipishaInitiateForm
from .forms import LipishaAcknowledgeForm

LOG = __import__('logging').getLogger('django')


class LipishaIpnView(View):
    """
    Process Lipisha IPN Callbacks
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LipishaIpnView, self).dispatch(request, *args, **kwargs)

    def validate_request(self, form_data):
        if not (form_data.get('api_key') == LIPISHA_API_KEY and
                form_data.get('api_signature') == LIPISHA_API_SIGNATURE):
            LOG.error("Lipisha. Check configured api_key and api_signature")
            raise SuspiciousOperation("Check Request Credentials")

    def post(self, request):
        response = {}
        form_class = None
        self.validate_request(request.POST)
        api_type = request.POST.get('api_type')
        if api_type == TYPE_ACKNOWLEDGE:
            form_class = LipishaAcknowledgeForm
        elif api_type == TYPE_INITIATE:
            form_class = LipishaInitiateForm
        if form_class is not None:
            transaction_status_code = STATUS_SUCCESS
            transaction_status = 'Processed'
            transaction_status_description = 'Status Processed'
            form = form_class(request.POST)
            if form.is_valid():
                form.process_payment()
            else:
                LOG.error('Error while processing payment')
                for error in form.errors:
                    LOG.error(error)
                transaction_status_code = STATUS_INITIATE_FAILURE
                transaction_status = 'Error'
                transaction_status_description = 'Error while processing payment'
            if api_type == TYPE_INITIATE:
                response = dict(
                     api_key=LIPISHA_API_KEY,
                    api_signature=LIPISHA_API_SIGNATURE,
                    api_version=form.cleaned_data['api_version'],
                    api_type=TYPE_RECEIPT,
                    transaction_reference=form.cleaned_data['transaction_reference'],
                    transaction_status_code=transaction_status_code,
                    transaction_status=transaction_status,
                    transaction_status_description=transaction_status_description
                )
        else:
            raise SuspiciousOperation
        return JsonResponse(response)

