#!/usr/bin/env python
# coding: utf8

import requests
from inc.misc.Alert import Alert
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def request(url, verbose=False, waittime=0):
    if verbose:
        print(Alert.info() + "Scraping '{}' ...".format(url))

    try:

        res = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        }, verify=False, timeout=10, allow_redirects=False)

        if res.status_code is 200 and verbose:
            print(Alert.success() + "Statuscode 200")

        if res.status_code > 200 and res.status_code < 500:
            print(Alert.warning() + "Statuscode {}".format(res.status_code))

        if res.status_code >= 500:
            print(Alert.error() + "Statuscode {}".format(res.status_code))

        if res.text is None or res.text is '':
            print(Alert.error() + "No content fetched... (WAF?)")

        if waittime > 0 and verbose:
            print(Alert.info() + "Waiting {} seconds...".format(waittime))

        if waittime > 0:
            time.sleep(waittime)
        return res.text

    except Exception as e:

        print(Alert.error() + "Exception while requesting victims url")
        sys.exit(1)
