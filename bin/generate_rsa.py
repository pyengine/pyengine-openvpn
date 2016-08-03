#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rsa
import os, sys

path = os.path.abspath(__file__ + '/../..')
if path not in sys.path:
    sys.path.append(path)

from identity import settings 

def createKey():
    (pubkey,  prikey) = rsa.newkeys(1024)

    f = open(settings.PUB_KEY_PATH,'w')
    pubkey_str = rsa.PublicKey.save_pkcs1(pubkey)
    f.write(pubkey_str)
    f.close()

    f = open(settings.PRI_KEY_PATH,'w')
    prikey_str = rsa.PrivateKey.save_pkcs1(prikey)
    f.write(prikey_str)
    f.close()


if __name__ == '__main__':
    createKey()
