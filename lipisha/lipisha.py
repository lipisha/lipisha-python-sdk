# -*- coding: utf-8 -*-

import json
try:
    from urllib.request import build_opener
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import build_opener
    from urllib import urlencode

from .api_config import API_METHOD_CONFIGURATION, PARAMETER_DEFAULTS
from .api_config import API_BASE_URL, API_SANDBOX_URL, DEFAULT_API_VERSION
from .api_config import DEFAULT_OPTIONAL_PARAMETERS


PRODUCTION_ENV = 'live'
SANDBOX_ENV = 'test'

PARAMETER_ERROR_TEMPLATE = 'API: {method}: `{name}` is required'
API_DOC_TEMPLATE = '''API Method: {method}

API_URL: {base_url}/{method}

DOCUMENTATION: http://developer.lipisha.com/index.php/app/launch/api_{method}

Required Parameters:

{required_parameters}

Optional Parameters:

{optional_parameters}

'''


def _make_title(v):
    return v.replace('_', ' ').title()

def _generate_api_method(
        method_name, required_parameters, optional_parameters):
    def api_method(self, **kwargs):
        for parameter in required_parameters:
            if parameter not in kwargs:
                if parameter not in PARAMETER_DEFAULTS:
                    msg = PARAMETER_ERROR_TEMPLATE.format(method=method_name,
                                                          name=parameter)
                    raise ValueError(msg)
                else:
                    kwargs.update({parameter: PARAMETER_DEFAULTS[parameter]})
        return self._make_api_call(method_name, **kwargs)
    req_params_list = '\n'.join([':param {}: {}'.format(p, _make_title(p))
                                 for p in required_parameters])
    optional_params = optional_parameters + DEFAULT_OPTIONAL_PARAMETERS
    opt_params_list = '\n'.join([':param {}: {}'.format(p, _make_title(p))
                                 for p in optional_params])
    method_doc = API_DOC_TEMPLATE.format(base_url=API_BASE_URL,
                                         method=method_name,
                                         required_parameters=req_params_list,
                                         optional_parameters=opt_params_list)
    api_method.__name__ = method_name
    api_method.__doc__ = method_doc
    return api_method


class Lipisha(object):

    '''API Client Implementation

    This class instantiates a client to the Lipisha API.
    Initialization parameters are defined below

    :param api_key: Lipisha API Key
    :param api_signature: Lipisha API Signature
    :param api_environment: This can either be "live" or "test".
                            Test environment will use the Lipisha sandbox
    :param api_version: Lipisha API Version (Defaults to `DEFAULT_API_VERSION`)
    :param opener_handlers: instances of handlers to customize urllib.build_opener
                            behaviour. this may be used to customize the how
                            connections to Lipisha are invoved e.g. Proxy connections..

    '''
    def __init__(self, api_key, api_signature,
                 api_environment=PRODUCTION_ENV,
                 api_version=DEFAULT_API_VERSION,
                 opener_handlers=[]):

        self.default_parameters = dict(api_key=api_key,
                                       api_signature=api_signature,
                                       api_version=api_version)
        _err = 'api_environment must be either `{}` or `{}'.format(
            PRODUCTION_ENV, SANDBOX_ENV)
        assert api_environment in (PRODUCTION_ENV, SANDBOX_ENV), _err
        self.api_base_url = (API_BASE_URL if
                             api_environment == PRODUCTION_ENV
                             else API_SANDBOX_URL)
        self.opener = build_opener(*opener_handlers)

    def _make_api_call(self, api_method, **kwargs):
        '''Fire API Call for named method.
        '''
        api_url = '/'.join((self.api_base_url, api_method))
        parameters = dict()
        parameters.update(self.default_parameters)
        parameters.update(kwargs)
        post_params = urlencode(parameters).encode('utf-8')
        response = self.opener.open(api_url, post_params)
        return json.loads(response.read().decode('utf-8'))


for api_method, required_params, optional_params in API_METHOD_CONFIGURATION:
    setattr(Lipisha,
            api_method,
            _generate_api_method(api_method, required_params,
                                 optional_params))
