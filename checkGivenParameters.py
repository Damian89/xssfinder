# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Damian Schwyrz


import sys

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, requires Python 3.x\n")
    sys.exit(1)

import requests
import urllib3
import time
import argparse
from urllib import parse
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
}

parser = argparse.ArgumentParser()

parser.add_argument(
    '-url',
    help='URL target',
    type=str,
    dest='url',
    default=None
)

parser.add_argument(
    '-payload',
    help='Define payload',
    type=str,
    dest='payload',
    default="9cdfb439c7876e703e307864c9167a15"
)

args = parser.parse_args()

if args.url is None:
    parser.print_help()
    sys.exit(1)

url = args.url
payload = args.payload

startTime = time.time()
time.clock()


def main():
    start = time.time()

    customParameters = extractCustomParameters()

    print("\033[91mScraping finished... found {} potential parameters\033[0m".format(len(customParameters)))
    print("")

    urlparsed = parse.urlparse(url)
    parameters_in_url = parse.parse_qsl(urlparsed.query)
    parameterkey_in_url = parse.parse_qs(urlparsed.query)
    scheme = urlparsed.scheme
    target = urlparsed.netloc
    path = urlparsed.path
    baseUrl = "{}://{}{}".format(scheme, target, path)
    addFoundParameterToTestset(customParameters, parameterkey_in_url, parameters_in_url)

    showSimpleProcessData(baseUrl, parameters_in_url, path, scheme, target)

    testUrlParams = prepareTestUrls(baseUrl, parameters_in_url)

    requestUrlAndCheckForReflection(testUrlParams)

    end = time.time()
    print("Process finished after: {} seconds".format(end - start))


def requestUrlAndCheckForReflection(testUrlParams):
    for testparam, testUrl in testUrlParams:
        try:
            res = requests.get(testUrl, headers=headers, verify=False, timeout=15, allow_redirects=False)

            print("Testing: {}".format(testUrl))
            print(" \033[92mStatus:\033[0m {}".format(res.status_code))

            if payload in res.text:
                print(" \033[31mParam:\033[0m {}".format(testparam))
                print(" \033[31mPayload found in http body.\033[0m")

        except Exception as e:
            print(e)
            print("Exception was thrown...")

        print("")


def showSimpleProcessData(baseUrl, parameters_in_url, path, scheme, target):
    print("\033[92mURL:\033[0m         {}".format(baseUrl))
    print("\033[92mScheme:\033[0m      {}".format(scheme))
    print("\033[92mTarget:\033[0m      {}".format(target))
    print("\033[92mPath:\033[0m        {}".format(path))
    print("")
    print("\033[92mThis parameters will be tested:\033[0m  ")
    for param, value in parameters_in_url:
        textAddon = ""

        if value is "XXX":
            textAddon = "\033[90m(found in DOM)\033[0m"

        print(" \033[94m{}\033[0m [{}] {}".format(param, value, textAddon))

    print("")


def addFoundParameterToTestset(customParameters, parameterkey_in_url, parameters_in_url):
    for param in customParameters:
        if param not in list(parameterkey_in_url):
            parameters_in_url.append([param, "XXX"])


def prepareTestUrls(baseUrl, parameters_in_url):
    manipulated = []
    testUrlParams = []

    for param1, value1 in parameters_in_url:
        testparam = ''
        testurl = baseUrl

        if param1 in manipulated:
            testurl = testurl + "?" + param1 + "=" + value1

        else:
            testparam = param1
            testurl = testurl + "?" + param1 + "=" + payload
            manipulated.append(param1)

        for param2, value2 in parameters_in_url:
            if param1 is param2:
                continue

            testurl = testurl + "&" + param2 + "=" + value2

        testUrlParams.append([testparam, testurl])

    return testUrlParams


def extractCustomParameters():
    customParameters = []

    try:
        print("\033[91mScraping URL...\033[0m")
        res = requests.get(url, headers=headers, verify=False, timeout=15, allow_redirects=False)
        content = res.text
        print(res.status_code)
        status = res.status_code
        soup = BeautifulSoup(content, 'html.parser')

        for input in soup.find_all("input"):
            if input.get("id") != None:
                customParameters.append(input.get("id"))

            if input.get("name") != None:
                customParameters.append(input.get("name"))

        for input in soup.find_all("select"):
            if input.get("id") != None:
                customParameters.append(input.get("id"))

            if input.get("name") != None:
                customParameters.append(input.get("name"))

        for input in soup.find_all("textarea"):
            if input.get("id") != None:
                customParameters.append(input.get("id"))

            if input.get("name") != None:
                customParameters.append(input.get("name"))

        for input in soup.find_all("checkbox"):
            if input.get("id") != None:
                customParameters.append(input.get("id"))

            if input.get("name") != None:
                customParameters.append(input.get("name"))

        for input in soup.find_all("button"):
            if input.get("id") != None:
                customParameters.append(input.get("id"))

            if input.get("name") != None:
                customParameters.append(input.get("name"))

    except Exception as e:
        pass

    return list(set(customParameters))


if __name__ == '__main__':
    main()
