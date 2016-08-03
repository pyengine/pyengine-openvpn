# Install and Configure OpenVPN's Server Environment

## Prerequisite

Keyword | Value     | Description
----    | ----      | ----
NET1 | route 10.1.0.0 255.255.255.0 | Expose network to client
COUNTRY | KR        | Key Country
PROVINCE | Seoul        | Key Province
CITY | Seoul        | Key City
ORG | My_Company    | Key Company
EMAIL | admin@example.com       | Key email
OU |  My_OrganizationUint| Key Organizational Unit


## Install OpenVPN package

~~~bash
apt-get update
apt-get install -y openvpn easy-rsa
~~~

# Configuration

## Copy configuration files

The example VPN server configuration file needs to be extracted to /etc/openvpn so we can incooporate it into our step. 

~~~bash
gunzip -c /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz > /etc/openvpn/server.conf
~~~


## Update server.conf

edit /etc/openvpn/server.conf

~~~text
port 1194
proto udp
dev tun

ca ca.crt
cert server.crt
key server.key

dh2048.pem

server 10.8.0.0 255.255.255.0

###########################################
# If you want to expose network to client #
# Add push command                        #
###########################################
push "${NET1}"

ifconfig-pool-persist ipp.txt

keepalive 10 120

comp-lzo

user nobody
group nogroup

persist-key
persist-tun

status openvpn-status.log

verb 3
~~~

## Packet Forwarding

OpenVPN should forward traffic to other machine.

~~~bash
sysctl -w net.ipv4.ip_forward=1
~~~

# Step 2. Create a Certificate Authority

## Configure and Build the Certificate Authority

It is now time to set up our own Certificate Authority (CA) and generate a certificate and key for the OpenVPN server. OpenVPN supports bidirectional authentication based on certificates, meaning that the client must authenticate the server certificate and the server must authenticate the client certificate before mutual trust is established. We will use Easy RSA's scripts we copied earlier to do this.

First copy over the Easy-RSA generation scripts.

~~~bash
cp -r /usr/share/easy-rsa/ /etc/openvpn
mkdir /etc/openvpn/easy-rsa/keys
~~~


Easy-RSA has a variables file we can edit to create certificates exclusive to our person, business, or whatever entity we choose. This information is copied to the certificates and keys, and will help identify the keys later.

edit /etc/openvpn/easy-rsa/vars

~~~text
# easy-rsa parameter settings

# NOTE: If you installed from an RPM,
# don't edit this file in place in
# /usr/share/openvpn/easy-rsa --
# instead, you should copy the whole
# easy-rsa directory to another location
# (such as /etc/openvpn) so that your
# edits will not be wiped out by a future
# OpenVPN package upgrade.

# This variable should point to
# the top level of the easy-rsa
# tree.
export EASY_RSA="`pwd`"

#
# This variable should point to
# the requested executables
#
export OPENSSL="openssl"
export PKCS11TOOL="pkcs11-tool"
export GREP="grep"


# This variable should point to
# the openssl.cnf file included
# with easy-rsa.
export KEY_CONFIG=`$EASY_RSA/whichopensslcnf $EASY_RSA`

# Edit this variable to point to
# your soon-to-be-created key
# directory.
#
# WARNING: clean-all will do
# a rm -rf on this directory
# so make sure you define
# it correctly!
export KEY_DIR="$EASY_RSA/keys"

# Issue rm -rf warning
echo NOTE: If you run ./clean-all, I will be doing a rm -rf on $KEY_DIR

# PKCS11 fixes
export PKCS11_MODULE_PATH="dummy"
export PKCS11_PIN="dummy"

# Increase this to 2048 if you
# are paranoid.  This will slow
# down TLS negotiation performance
# as well as the one-time DH parms
# generation process.
export KEY_SIZE=2048

# In how many days should the root CA key expire?
export CA_EXPIRE=3650

# In how many days should certificates expire?
export KEY_EXPIRE=3650

# These are the default values for fields
# which will be placed in the certificate.
# Don't leave any of these fields blank.
export KEY_COUNTRY="${COUNTRY}"
export KEY_PROVINCE="${PROVINCE}"
export KEY_CITY="${CITY}"
export KEY_ORG="${ORG}"
export KEY_EMAIL="${EMAIL}"
export KEY_OU="${OU}"

# X509 Subject Field
export KEY_NAME="server"

# PKCS11 Smart Card
# export PKCS11_MODULE_PATH="/usr/lib/changeme.so"
# export PKCS11_PIN=1234

# If you'd like to sign all keys with the same Common Name, uncomment the KEY_CN export below
# You will also need to make sure your OpenVPN server config has the duplicate-cn option set
# export KEY_CN="CommonName"
~~~

We need to generate the Diffie-Hellman parameters; this can take several minutes.

~~~bash
openssl dhparam -out /etc/openvpn/dh2048.pem 2048
~~~

Now let's change directories so that we're working directly out of where we moved Easy-RSA's scripts to earlier in Step 2.

~~~bash
cd /etc/openvpn/easy-rsa
. ./vars
./clean-all
./build-ca
~~~
