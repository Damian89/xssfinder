#!/usr/bin/env python
# coding: utf8

import requests

from inc.misc.Alert import Alert
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def request(url, payload, waittime=0, showrequest=False, cookies=None):
    if showrequest:
        print(Alert.info() + "Scraping '{}' ...".format(url))

    try:

        res = make_request(url, cookies)

        if res.history and showrequest:
            print(Alert.warning() + "Request was redirected")
            print(Alert.success() + "Final destination: {} ({})".format(res.url, res.status_code))

        if res.history and payload not in res.url and showrequest:
            print(Alert.warning() + "Sending new corrected request...")
            print(Alert.info() + "Corrected request: " + res.url + payload)

            confirm(prompt=Alert.info() + "Do you want to proceed? Please check the new url and use verbose mode!",
                    resp=True)

        if res.history and payload not in res.url:
            res = make_request(res.url + payload, cookies)

        if res.status_code is 200:
            print(Alert.success() + "Statuscode 200")
            print(url, file=sys.stderr)

        if res.status_code > 200 and res.status_code < 500:
            print(Alert.warning() + "Statuscode {}".format(res.status_code))
            print(url, file=sys.stderr)

        if res.status_code >= 500:
            print(Alert.error() + "Statuscode {}".format(res.status_code))
            print(url, file=sys.stderr)

        if res.text is None or res.text is '':
            print(Alert.error() + "No content fetched... (WAF?)")
        else:
            print(Alert.success() + "Content Length: {}".format(len(res.text)))

        if waittime > 0:
            print(Alert.info() + "Waiting {} seconds...".format(waittime))
            time.sleep(waittime)

        return res.text

    except Exception as e:

        print(Alert.error() + "Exception:")
        print(Alert.error() + e)

        sys.exit(1)


def make_request(url, cookies=None):
    res = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'accept-language': 'en-US,en;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': url,
        'cookie': cookies,
    }, verify=False, timeout=15, allow_redirects=True)

    return res


""" Stolen from http://code.activestate.com/recipes/541096-prompt-the-user-for-confirmation/ """


def confirm(prompt=None, resp=False):
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            sys.exit(1)
