#!/usr/bin/env python
#-*- coding: utf-8 -*-

try:
    import json
except ImportError:
    import simplesjon as json


def get(filename):
    success = True
    try:
        config = file(filename)
        accounts = json.load(config)
        config.close()
    except Exception:
        success = False
        accounts = None

    return accounts, success
