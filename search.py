from urllib import urlencode
from urllib2 import urlopen, Request
import os
import sys
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

HOST = config.get("global", "host")
PORT = config.getint("global", "port")
ACCOUNT = config.get("global", "account")
PASSPORT = config.get("global", "passport")
PASSWORD = config.get("global", "password")
SID = config.get("global", "sid")

API_URL = "http://%s:%d/portal/apis" % (HOST, PORT)


def validate():
    if len(HOST) < 1:
        print "Please provide a the hostname of the NAS (e.g. nas.local, 192.168.0.100, etc)"
    if len(ACCOUNT) < 1:
        print "Please provide a username (account)"
    if len(PASSWORD) < 1 and len(PASSPORT) < 1:
        print "Please provide password or passport"


def fetch_sid():
    url = API_URL + "/login.cgi?act=login"

    if len(PASSPORT) > 0:
        post_data = urlencode({'account': ACCOUNT, 'passport': PASSPORT})
    else:
        post_data = urlencode({'account': ACCOUNT, 'password': PASSWORD})

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    request = urlopen(Request(url, headers=headers), post_data)
    response = json.loads(request.read())

    if response['success'] is False:
        print "Failed to fetch SID, error message: '%s', code: '%d'" % (response['error_msg'], response['error_code'])
        sys.exit(1)

    return response['sid']


def update_sid(new_sid):
    config.set("global", "sid", new_sid)
    with open('config.ini', 'wb') as configfile:
        config.write(configfile)


def search(param):
    params = urlencode({'sid': SID, 'act': 'search', 'query': param})
    url = API_URL + "/fileSearch/filesearch.cgi?%s"

    request = urlopen(url % (params))
    result = json.loads(request.read())

    # if result['success'] is False:
    #     print "Something went wrong..."
    #     print result

    # if result['toomany'] is True:
    #     print "Too many results to display all..."
    #     print result

    return result

validate()

if len(SID) < 1:
    new_sid = fetch_sid()
    SID = new_sid
    update_sid(new_sid)


args = " ".join(sys.argv[1:])
if len(args) < 1:
    sys.exit(json.dumps({'success': False, 'error_msg': 'No search terms provided'}))

print json.dumps(search(args))
