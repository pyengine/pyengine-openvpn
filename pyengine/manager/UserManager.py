from django.contrib.auth.hashers import make_password
from pyengine.lib import utils
from pyengine.lib import config
from pyengine.lib.error import *
from pyengine.manager import Manager 

class UserManager(Manager):

    GLOBAL_CONF = config.getGlobalConfig()

    def createUser(self, params):
        user_dao = self.locator.getDAO('user') 

        if user_dao.isExist(user_id=params['user_id']):
            raise ERROR_EXIST_RESOURCE(key='user_id', value=params['user_id'])

        if not utils.checkIDFormat(params['user_id']):
            raise ERROR_INVALID_ID_FORMAT()

        if not utils.checkPasswordFormat(params['password']):
            raise ERROR_INVALID_PASSWORD_FORMAT()

        dic = {}
        dic['user_id'] = params['user_id']
        dic['password'] = make_password(params['password'])

        if params.has_key('name'):
            dic['name'] = params['name']

        if params.has_key('email'):
            dic['email'] = params['email']

        if params.has_key('language'):
            dic['language'] = params['language']
        else:
            dic['language'] = self.GLOBAL_CONF['DEFAULT_LANGUAGE']

        if params.has_key('timezone'):
            dic['timezone'] = params['timezone']
        else:
            dic['timezone'] = self.GLOBAL_CONF['DEFAULT_TIMEZONE']

        if params.has_key('group_id'):
            group_dao = self.locator.getDAO('group')

            groups = group_dao.getVOfromKey(uuid=params['group_id'])

            if groups.count() == 0:
                raise ERROR_INVALID_PARAMETER(key='group_id', value=params['group_id'])

            dic['group'] = groups[0]

        user = user_dao.insert(dic)

        return self.locator.getInfo('UserInfo', user)

    def updateUser(self, params):
        user_dao = self.locator.getDAO('user') 

        if not user_dao.isExist(user_id=params['user_id']):
            raise ERROR_INVALID_PARAMETER(key='user_id', value=params['user_id'])

        dic = {}

        if params.has_key('password'):
            if not utils.checkPasswordFormat(params['password']):
                raise ERROR_INVALID_PASSWORD_FORMAT()

            dic['password'] = make_password(params['password'])

        if params.has_key('name'):
            dic['name'] = params['name']

        if params.has_key('state'):
            dic['state'] = params['state']

        if params.has_key('email'):
            dic['email'] = params['email']

        if params.has_key('language'):
            dic['language'] = params['language']

        if params.has_key('timezone'):
            dic['timezone'] = params['timezone']

        if params.has_key('group_id'):
            group_dao = self.locator.getDAO('group')

            groups = group_dao.getVOfromKey(uuid=params['group_id'])

            if groups.count() == 0:
                raise ERROR_INVALID_PARAMETER(key='group_id', value=params['group_id'])

            dic['group'] = groups[0]

        user = user_dao.update(params['user_id'], dic, 'user_id')

        return self.locator.getInfo('UserInfo', user)

    def deleteUser(self, params):
        user_dao = self.locator.getDAO('user') 

        users = user_dao.getVOfromKey(user_id=params['user_id'])

        if users.count() == 0:
            raise ERROR_NOT_FOUND(key='user_id', value=params['user_id'])

        users.delete()

        return {}

    def enableUser(self, params):
        params['state'] = 'enable'

        return self.updateUser(params)

    def disableUser(self, params):
        params['state'] = 'disable'

        return self.updateUser(params)

    def getUser(self, params):
        user_dao = self.locator.getDAO('user')

        users = user_dao.getVOfromKey(user_id=params['user_id'])

        if users.count() == 0:
            raise ERROR_NOT_FOUND(key='user_id', value=params['user_id'])

        return self.locator.getInfo('UserInfo', users[0])

    def listUsers(self, search, search_or, sort, page, res_params):
        user_dao = self.locator.getDAO('user')

        if len(res_params) > 0:
            related_parent = []

            for p in res_params:
                if p == 'group_name':
                    related_parent.append('group')
        else:
            # DAO - Join Example
            # parent_model = ['<model_name>']
            # parent_parent_model = ['<model_name.model_name>']
            related_parent = ['group']

        output = []
        (users, total_count) = user_dao.select(search=search, search_or=search_or, sort=sort, page=page, related_parent=related_parent)

        for user in users:
            user_info = self.locator.getInfo('UserInfo', user, res_params=res_params)
            output.append(user_info)

        return (output, total_count)
