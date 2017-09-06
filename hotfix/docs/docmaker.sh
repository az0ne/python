#!/usr/bin/env bash

# PROJECT_HOME='/cygdrive/e/wxd/projects/20160305'
# PACKAGE_HOME='../mz_platform'
# docDestDir='mzPlatformDoc'

# export DJANGO_SETTINGS_MODULE=maiziedu_website.settings
# oripypath=$PYTHONPATH
# export PYTHONPATH=$PYTHONPATH:$PROJECT_HOME
# # echo `find doc -name "*.rst"|grep -v index.rst`

# sphinx-apidoc -Mfe -o doc $PACKAGE_HOME
# # sphinx-apidoc -Mfe -o doc  ../mz_platform
# make -C doc html

# rm -rf $docDestDir/*
# cp -R doc/_build/html/* $docDestDir

# export PYTHONPATH=$oripypath
# # /cygdrive/e/wxd/projects/20160305/mz_platform

doxygen
