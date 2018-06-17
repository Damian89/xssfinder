#!/usr/bin/env python
# coding: utf8

from inc.misc.Alert import Alert
import re


def getInterestingParameters(content):
    customParameters = []

    """ Whats this? Extracting all data-* attributes ;) """
    dataattributes = list(set(re.findall(' data-([a-zA-Z0-9\-\_]+)', content)))

    """ Get all ids of every element ;) """
    elementids_1 = list(set(re.findall(' id="([a-zA-Z0-9\-\_]+)"', content)))
    elementids_2 = list(set(re.findall(' id=\'([a-zA-Z0-9\-\_]+)\'', content)))

    """ Get all names of every element ;) """
    elementnames_1 = list(set(re.findall(' name="([a-zA-Z0-9\-\_]+)"', content)))
    elementnames_2 = list(set(re.findall(' name=\'([a-zA-Z0-9\-\_]+)\'', content)))

    return list(set(customParameters + dataattributes + elementids_1 + elementids_2 + elementnames_1 + elementnames_2))


def reportParameterFindingInDom(interestingParameters):
    interestingParametersCount = len(interestingParameters)

    if interestingParametersCount > 0:
        print(Alert.success() + "{} parameters found in HTML response".format(interestingParametersCount))

    if interestingParametersCount is 0:
        print(Alert.info() + "No parameters found in HTML response")

    for iterator, param in enumerate(interestingParameters):
        print(Alert.info() + "Parameter #{}: {}".format((iterator + 1), param))


def reportParameterFindingInUrl(parametersInUrl):
    interestingParametersCount = len(parametersInUrl)

    if interestingParametersCount > 0:
        print(Alert.success() + "{} parameters found in URL".format(interestingParametersCount))

    if interestingParametersCount is 0:
        print(Alert.info() + "No parameters found in URL")

    for iterator, param in enumerate(parametersInUrl):
        print(Alert.info() + "Parameter #{}: {}".format((iterator + 1), param))
