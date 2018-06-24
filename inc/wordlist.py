#!/usr/bin/env python
# coding: utf8

import os
import sys

from inc.misc.Alert import Alert


def getParamsFromWordList(withWordList, paramlist):
    if withWordList == False:
        print(Alert.warning() + "No wordlist specified - we will use only custom parameters found in HTML response or URL")
        return []

    if (os.path.exists(paramlist) == False):
        print(Alert.error() + "Wordlist specified but not found on filesystem")
        sys.exit(1)

    print(Alert.info() + "Reading wordlist...")
    return open(paramlist, 'r').read().splitlines()



def combineFoundParameters(wordlistParameters, interestingParameters, parametersInUrl):

    print(Alert.info() + "Custom parameters:     {}".format(len(interestingParameters)))
    print(Alert.info() + "Inital get parameters: {}".format(len(parametersInUrl)))
    print(Alert.info() + "Wordlist parameters:   {}".format(len(wordlistParameters)))

    combinedParameters = list(set(wordlistParameters + interestingParameters + parametersInUrl))

    print(Alert.success() + "Deleting duplicates...")
    print(Alert.info() + "Using {} unique parameters".format(len(combinedParameters)))

    return combinedParameters
