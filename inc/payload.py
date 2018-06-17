#!/usr/bin/env python
# coding: utf8

import hashlib

from inc.misc.Alert import Alert


def createOnePayloadPerParam(parameters, extendedchar=""):
    hashes = []
    parametersPayloaded = []

    for param in parameters:
        hash = "{}{}a".format(hashlib.md5(param.encode('utf-8')).hexdigest()[0:7], extendedchar)

        if hash in hashes:
            print(Alert.warning() + "Duplicate payload identifier found... {}".format(hash))

        parametersPayloaded.append([
            param,
            hash
        ])

        hashes.append(hash)
    return parametersPayloaded
