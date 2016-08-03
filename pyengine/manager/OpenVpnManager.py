from pyengine.lib import utils
from pyengine.lib import config
from pyengine.lib.error import *
from pyengine.manager import Manager

import os
import subprocess

KEY_DIR = "/etc/openvpn/easy-rsa/keys"
TARGET_DIR = "/opt/pyengine-openvpn/static/keys"

class OpenVpnManager(Manager):

    GLOBAL_CONF = config.getGlobalConfig()
    SERVER = GLOBAL_CONF['SERVER_ADDRESS']
    URL = "http://%s/static/keys" % GLOBAL_CONF['SERVER_ADDRESS']

    def createKey(self, params):
        """
        To create openvpn key, we need root permission
        add /etc/sudoer
        www-data ALL=(ALL) NOPASSWD: ALL
        """
        name = params['user_name']
        email = params['emailAddress']
        if params.has_key('organizationUnitName'):
            ou = params['organizationUnitName']
        else:
            ou = 'My Organization'

        dao = self.locator.getDAO('openvpn_user')
        users = dao.getVOfromKey(name=name)
        if users.count() > 0:
            raise ERROR_EXIST_RESOURCE(key=name, value=name)

       # Execute Cmd
        cmd = ["sudo", "/etc/openvpn/easy-rsa/pyengine-build-key.sh", name, email, ou]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)
        self.logger.debug("%s" % result)

        ca = "%s/ca.crt" % KEY_DIR
        crt = "%s/%s.crt" % (KEY_DIR, params['user_name'])
        key = "%s/%s.key" % (KEY_DIR, params['user_name'])
        client_content = """
client
dev tun
proto udp
remote %s 1194
resolv-retry infinite
nobind
user nobody
group nogroup
persist-key
persist-tun
ca %s.ca
cert %s.crt
key %s.key
ns-cert-type server
comp-lzo
verb 3
""" % (self.SERVER, params['user_name'],params['user_name'], params['user_name'])

        # Copy key files to destination

        USER_DIR = "%s/%s" % (TARGET_DIR, params['user_name'])
        USER_TAR = "%s/%s.tar" % (TARGET_DIR, params['user_name'])

        cmd = ["sudo", "rm", "-rf", USER_DIR]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)

        cmd = ["sudo", "mkdir", USER_DIR]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)

        cmd = ["sudo", "cp", ca, "%s/%s.ca" % (USER_DIR, params['user_name'])]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)

        cmd = ["sudo", "cp", crt, "%s/%s.crt" % (USER_DIR, params['user_name'])]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)

        cmd = ["sudo", "cp", key, "%s/%s.key" % (USER_DIR, params['user_name'])]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)

        temp_path = "/tmp/client.ovpn"
        client_path = "%s/client.ovpn" % USER_DIR
        fp = open(temp_path, 'w')
        fp.write(client_content)
        fp.close()

        cmd = ["sudo", "cp", "/tmp/client.ovpn", client_path]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)

        cmd = ["sudo", "tar", "-C", TARGET_DIR, "-cvf", USER_TAR, params['user_name']]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)

        cmd = ["sudo", "rm", "-rf", USER_DIR]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)


        result = {"url":"%s/%s.tar" % (self.URL, params['user_name']),
                    "openvpn_binary":"%s/openvpn-install-2.3.6-I603-i686.exe" % self.URL}

        # update DB
        dic = {}
        dic['name'] = name
        dic['ou'] = ou
        dic['email'] = email
        dic['ca'] = ca
        dic['crt'] = crt
        dic['key'] = key
        dic['ovpn'] = client_content
        user = dao.insert(dic)

        return result

