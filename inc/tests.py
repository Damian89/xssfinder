#!/usr/bin/env python
# coding: utf8

from inc.misc.Alert import Alert
import sys


def initialReflectionTest(content, modeextended):
    paramWasReflected = False
    killScript = False

    if "r4nd0mStr1ng" in content:
        paramWasReflected = True
        print(Alert.warning() + "Random parameter (\"r4nd0mStr1ng\") was reflected in the inital request.")
        print(Alert.warning() + "This will result in a lot false results, if you are not using extended mode!")

    if modeextended == True:
        print(Alert.success() + "Thank god! You are using the extended mode!")

    elif modeextended == False and paramWasReflected:
        killScript = True
        print(Alert.warning() + "You should use the extended test mode!")

    if killScript:
        sys.exit(1)


def reportReflection(content, chunk):
    for param, payload in chunk:
        if payload in content:
            print(Alert.reflection() + "Parameter '{}' with value '{}'".format(param, payload))
