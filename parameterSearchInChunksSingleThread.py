#!/usr/bin/env python
# coding: utf8

import sys

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, Python 3.x is required\n")
    sys.exit(1)

import time
from inc.misc.Alert import Alert
from inc.arguments import parseArguments, validateArguments, getArguments
from inc.requests import request
from inc.paramfinder import getInterestingParameters, reportParameterFindingInDom, reportParameterFindingInUrl
from inc.wordlist import getParamsFromWordList, combineFoundParameters
from inc.chunk import makeChunks
from inc.payload import createOnePayloadPerParam
from inc.url import constructGetQuery, deconstructUrl
from inc.tests import initialReflectionTest, reportReflection


def main():
    start = time.time()

    """ Parse input arguments """
    args = parseArguments()

    """ We need some of them in every case """
    validateArguments(args)

    """ Save input arguments """
    withWordList, url, verbose, extended, paramlist, chunksize, extendedchar, waittime = getArguments(args)

    """ Deconstruct input url into base url without query string and list of query parameters """
    baseUrl, parametersInUrl = deconstructUrl(url)

    initialRequestUrl = baseUrl + "?r4nd0mStr1ng=gn1rtSm0dn4r"

    """ Make inital paramter to base url using some bogus random string to verify that its not reflected """
    content = request(initialRequestUrl, payload="?r4nd0mStr1ng=gn1rtSm0dn4r", waittime=waittime, showrequest=True)
    initialReflectionTest(content, extended)

    """ Extract interesting parameters based on input fields, textareas, ... """
    interestingParameters = getInterestingParameters(content)
    reportParameterFindingInDom(interestingParameters)
    reportParameterFindingInUrl(parametersInUrl)

    """ Get our ~2500 word parameter list """
    wordlistParameters = getParamsFromWordList(withWordList, paramlist)

    """ Combine all parameters (wordlist, params found in html response and parameters from url """
    parameters = combineFoundParameters(wordlistParameters, interestingParameters, parametersInUrl)

    """ Add a payload to every parameter (necessary to detect a certain reflected parameter) """
    parametersPayloaded = createOnePayloadPerParam(parameters, extendedchar)

    """ Create chunks of a given size... this reduces the number of requests needed to check all parameters. """
    chunkedParmeterList = makeChunks(parametersPayloaded, chunksize)

    """ Now iterate through every chunk"""
    for iterator, chunk in enumerate(chunkedParmeterList):

        print(Alert.info() + "Request #{} started...".format(iterator + 1))

        """ Construct our test url with parameter-value string """
        getQuery = constructGetQuery(chunk)
        testUrl = "{}?{}".format(baseUrl, getQuery)

        """ Get the html response """
        content = request(testUrl, payload="?" + getQuery, waittime=waittime, showrequest=verbose)

        """ Check if one of the current chunk payloads was found in the html response, if so report..."""
        reportReflection(content, chunk)

        print("")

    """ Small reminder for non extended mode """
    if extended == False:
        print(Alert.info()
              + "If some reflected parameters were found using the default mode, I advice you too use the "
                "extended mode with some special characters like double quote, 'less than' or 'greater than' "
                "to check if those characters are reflected as well without sanitization: --extended -extendedchar '><'")

    end = time.time()
    print("Process finished after: {} seconds".format(end - start))


if __name__ == '__main__':
    main()
