#!/usr/bin/env python
# coding: utf8

from inc.misc.Alert import Alert
import re


def getInterestingParameters(content):
    customParameters = []

    """ Whats this? Extracting all data-* attributes ;) """
    dataattributes = list(set(re.findall(' data-([a-zA-Z0-9\-\_]+)', content)))

    """ Get all ids and names of every element ;) """
    elements = list(set(re.findall(' (?:name|id)\s+?=\s+?["\']?([a-zA-Z0-9\-\_]+)["\']?', content)))

    """ Get all js variables from content """
    vars = list(set(re.findall('var\s+?([a-zA-Z0-9\-\_]+)\s+?=', content)))

    return list(set(customParameters + dataattributes + elements + vars))


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
