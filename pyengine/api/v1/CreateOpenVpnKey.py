import pytz
from pyengine.lib.error import *
from pyengine.lib.command import Command

class CreateOpenVpnKey(Command):

    # Request Parameter Info
    req_params = {
        'user_name'             : ('r', 'str'),
        'organizationUnitName'  : ('o', 'str'),
        'emailAddress'          : ('r', 'str'),
    }

    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        mgr = self.locator.getManager('OpenVpnManager')

        info = mgr.createKey(self.params)

        return info

