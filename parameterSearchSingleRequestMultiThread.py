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

import os
import threading
import queue
import requests
import itertools
import urllib3
import time
import random
import argparse
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
    '-paramlist',
    help='Path to param list',
    type=str,
    dest='paramlist',
    default=None
)

parser.add_argument(
    '-threads',
    help='Max. threads (default: 10)',
    type=int,
    dest='threads',
    default=10
)

parser.add_argument(
    '-timeout',
    help='Stop script after this timeout in seconds (default: 3600)',
    type=int,
    dest='timeout',
    default=3600
)

parser.add_argument(
    '-payload',
    help='Ident payload - keep in mind some websites reflect the requested url, this may result in a lot false results',
    type=str,
    dest='ident',
    default='9cdfb439c7876e7"03e307864c9167a15'
)

parser.add_argument(
    '--verbose',
    nargs='?',
    const=True,
    help='Use verbose mode?',
    dest='verbose',
    default=False
)

parser.add_argument(
    '--extended',
    nargs='?',
    const=True,
    help='Use extended payload tests',
    dest='extended',
    default=False
)

args = parser.parse_args()

if args.url is None:
    parser.print_help()
    sys.exit(1)

use_wordlist = True

if args.paramlist is None:
    print("No wordlist specified!")
    use_wordlist = False

url = args.url
verbose = args.verbose
ident = args.ident
extended = args.extended
paramlist = args.paramlist
maxThreads = args.threads
timeout = args.timeout

payloads = []

if "'" not in ident:
    payloads.append("9cd'" + ident)

if '"' not in ident:
    payloads.append('9cd"' + ident)

if '>' not in ident:
    payloads.append('9cd>' + ident)

if '<' not in ident:
    payloads.append('9cd<' + ident)

customParameters = []

try:
    print("Scraping {}...".format(url))
    res = requests.get(url, headers=headers, verify=False, timeout=15, allow_redirects=False)
    content = res.text
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

print("Scraping finished... found {} potential parameters".format(len(customParameters)))

params = []

if use_wordlist:
    if (os.path.exists(paramlist) == False):
        print("Paramlist not found...")
        sys.exit(1)

    params = open(paramlist, 'r').read().splitlines()

params = list(set(customParameters + params))

if use_wordlist == False:
    print("Following parameters found:")
    print(params)

param_payload_perms = list(itertools.product(params, [ident]))

random.shuffle(param_payload_perms)

print("Initial requests planned: {}".format(len(param_payload_perms)))

requestsMade = 0
startTime = time.time()
time.clock()


class WorkerThread(threading.Thread):
    def __init__(self, queue, tid):
        threading.Thread.__init__(self)
        self.queue = queue
        self.tid = tid

    def run(self):

        global requestsMade

        while (queue.Empty() != True):
            elapsed = time.time() - startTime
            if (timeout > 1 and elapsed >= timeout):
                print("Timeout reached... exiting...")
                self.queue.task_done()
                return

            # Check if items in queue
            try:
                param, payload = self.queue.get(timeout=2)
            except queue.Empty:
                return

            # check auth data
            try:

                if "?" in url:
                    testUrl = url + "&" + param + "=" + payload
                else:
                    testUrl = url + "?" + param + "=" + payload

                res = requests.get(testUrl, headers=headers, verify=False, timeout=15, allow_redirects=False)
                time.sleep(1)

            except Exception as e:
                # Just in case we have a valid exception, because requests failed not by Timeout or MaxRetries,
                # force thread to stop... you will have to check this error out...
                print(e)
                print(
                    "Unknown exception caught... to prevent infinite loops, thread has to stop..."
                )

                return

            requestsMade += 1

            if requestsMade % 250 == 0:
                print("Requests made: {}".format(requestsMade))

            if payload in res.text:

                if verbose is False:
                    print("\033[1m\033[92mPotential reflected parameter found: {}\033[0m".format(param))

                if verbose is True:
                    print("\033[1m\033[92mPotential reflected parameter found:\033[0m")
                    print(" Status:     {}".format(res.status_code))
                    print(" Parameter:  {}".format(param))
                    print(" Payload:    {}".format(payload))
                    print(" URL:        {}".format(testUrl))

                if payload is not ident:
                    print(" \033[4m\033[91mUnfiltered parameter found: {}\033[0m".format(param))

                if payload is ident and extended is True:
                    if verbose is True:
                        print(" \033[1m\033[94mPutting extended tests in queue for this reflected parameter\033[0m")

                    extended_test_params = itertools.product([param], payloads)

                    for extended_test in extended_test_params:
                        self.queue.put(extended_test)

            self.queue.task_done()


def main():
    start = time.time()
    queueAll = queue.Queue()

    threads = []

    print("Starting {} workers...".format(maxThreads))
    for i in range(0, maxThreads):
        worker = WorkerThread(queueAll, i)
        worker.setDaemon(True)
        worker.start()
        threads.append(worker)

    for param_payload in param_payload_perms:
        queueAll.put(param_payload)

    for item in threads:
        item.join()

    end = time.time()
    print("Process finished after: {} seconds".format(end - start))


if __name__ == '__main__':
    main()
