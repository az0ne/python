Guide for deploy
====================

config centos
--------------------

    $yum install mysql-server libmysqld-dev libmysqlclient-dev
    $yum install python-dev
    $yum install nginx
    $yum install python-pip
    $yum install python-virtualenv
    $pip install virtualenvwrapper

deploy
----------------------

    $mkdir /home/www/
    $cd /home/www/
    $virtualenv --no-site-packages microoh.com
    $cd microoh.com/
    $source bin/activate
    $svn -co <repository> -username
    $cd reposictory
    $pip install -r requirements.pip

ADVISE FOR FATHER DEPLOY DEVELOPMENT::
------------------------------------------

1. use ansible to deploy project automatically

2. Use docker to build virtual envs

3. use supervisor to handle server work process.

!!!WARNINGS!!!
===================

1. root can not be used in production envs

2. firewall should be will configured


