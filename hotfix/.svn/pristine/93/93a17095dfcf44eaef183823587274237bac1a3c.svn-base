#!/usr/bin/env python
# encoding: utf-8
# vim: set et sw=4 ts=4 sts=4 fenc=utf-8
# Author: YuanLin

"""
    Using fabric to deploy to staging server and production server
    --------------------------------------------------------------

    - Local:
    1. Commit latest code
    2. Push to local <repository> server

    - Staging:
    1. Download latest code from <repository> server
    2. Checkout specified branch
    3. Work on project virtualenv
    4. Install requirentments
    5. Restart server

    - Production:
    1. Download latest code from <repository> server
    2. Checkout specified branch
    3. Work on project virtualenv
    4. Install requirentments
    5. Restart server
"""


from fabric.api import local, settings, abort, cd, run, env, prefix, roles
from fabric.contrib.console import confirm


