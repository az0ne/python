#!/usr/bin/env python
# coding=utf-8
__author__ = 'Cairenjie <crj93106@gmail.com>'
__version__ = (0, 0, 1)
__status__ = 'develop'
__date__ = 'Thu Jul 23 02:15:37 2015'

"""
logging package for python which store the logs to MongoDB
"""

from l2m import L2M, MONGODB_DEFAULT_CONFIG
from mongodbhandler import MongodbHandler
from basehandler import BaseHandler
from levels import Levels

__all__ = [L2M, MONGODB_DEFAULT_CONFIG, MongodbHandler]
