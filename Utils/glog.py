#!/usr/bin/python3
# encoding: utf-8


import logging

logger = None


def initlog(text=None, quite=False):
    global logger
    logger = logging.getLogger(text)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if quite is True:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def getlog():
    global logger
    return logger
