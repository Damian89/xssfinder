#!/usr/bin/env python
# coding: utf8

from bs4 import BeautifulSoup
from inc.misc.Alert import Alert
import re


def getInterestingParameters(content):
    customParameters = []

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

    dataattributes = list(set(re.findall(' data-([a-zA-Z0-9\-\_]+)', content)))

    return customParameters+dataattributes


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
