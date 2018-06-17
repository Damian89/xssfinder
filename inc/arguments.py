#!/usr/bin/env python
# coding: utf8

from inc.misc.Alert import Alert
import sys
import argparse


def validateArguments(args):
    if args.url is None:
        print(Alert.error() + "URL missing")
        sys.exit(1)

    if args.extended is True and (args.extendedchar is None or args.extendedchar is "") :
        print(Alert.error() + "Please specify a character for extended tests (e.g. > or <)")
        sys.exit(1)


def usingWordlist(args):
    use_wordlist = True

    if args.paramlist is None:
        use_wordlist = False

    return use_wordlist


def parseArguments():
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
        '-chunksize',
        help='Chunksize for parameters tested in one request (default: 75)',
        type=int,
        dest='chunksize',
        default=75
    )

    parser.add_argument(
        '-wait',
        help='Wait time between requests in seconds (default: 0)',
        type=int,
        dest='waittime',
        default=0
    )

    parser.add_argument(
        '--extended',
        nargs='?',
        const=True,
        help='Use extended payload tests',
        dest='extended',
        default=False
    )

    parser.add_argument(
        '-extendedchar',
        nargs='?',
        help='Character or String for extended tests',
        dest='extendedchar',
        default=""
    )

    parser.add_argument(
        '--verbose',
        nargs='?',
        const=True,
        help='Use verbose mode?',
        dest='verbose',
        default=False
    )

    return parser.parse_args()


def getArguments(args):
    withWordList = usingWordlist(args)
    url = args.url
    verbose = args.verbose
    extended = args.extended
    paramlist = args.paramlist
    chunksize = args.chunksize
    extendedchar = args.extendedchar
    waittime = args.waittime

    return withWordList, url, verbose, extended, paramlist, chunksize, extendedchar, waittime
