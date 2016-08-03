#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rsa
import os, sys

path = os.path.abspath(__file__ + '/../..')
if path not in sys.path:
    sys.path.append(path)

from identity import settings 

def loadKey():
    f = open(settings.PUB_KEY_PATH, 'r')
    pubkey_str = f.read()
    f.close()

    pubkey = rsa.PublicKey.load_pkcs1(pubkey_str)
    print pubkey

    f = open(settings.PRI_KEY_PATH, 'r')
    prikey_str = f.read()
    f.close()

    prikey = rsa.PrivateKey.load_pkcs1(prikey_str)
    print prikey


if __name__ == '__main__':
    loadKey()
