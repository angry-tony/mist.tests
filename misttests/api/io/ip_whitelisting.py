from misttests.api.helpers import *
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_whitelist_ips_no_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.whitelist_ips(api_token='').post()
    assert_response_unauthorized(response)
    print "Success!!!"
