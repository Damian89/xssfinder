#!/usr/bin/env python
# coding: utf8

from itertools import islice
from inc.misc.Alert import Alert

def makeChunks(listarr, size):
    listarr = iter(listarr)
    chunked = list(iter(lambda: tuple(islice(listarr, size)), ()))

    print(Alert.success()+"{} chunks with {} elements per chunk created".format(len(chunked),size))

    return chunked