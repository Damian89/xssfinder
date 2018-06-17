#!/usr/bin/env python
# coding: utf8

from urllib import parse


def constructGetQuery(tuplelist):
    query = ''

    for param, value in tuplelist:
        query = "{}&{}={}".format(query, param, value)

    return query[1:]


def deconstructUrl(url):
    urlparsed = parse.urlparse(url)
    parameterkey_in_url = parse.parse_qs(urlparsed.query)
    scheme = urlparsed.scheme
    target = urlparsed.netloc
    path = urlparsed.path
    baseUrl = "{}://{}{}".format(scheme, target, path)

    return baseUrl, list(parameterkey_in_url)
