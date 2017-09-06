# -*- coding: utf-8 -*-

import os, sys, django

if django.VERSION[1] > 5:
#    pwd = os.path.dirname(os.path.realpath(__file__))
#    sys.path.append(pwd+"/..")
    sys.path.append("/var/www/xadmin.com")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    django.setup()

import datetime, calc_fxsys_data


if __name__ == '__main__':
    args = sys.argv
    print args
    print 'parameter is eg: 2017-03-17 frozen/rebate/onlyrebate'
    if len(args) > 1:
        try:
            today_datetime = datetime.datetime.strptime(args[1], "%Y-%m-%d")
        except :
            print '时间格式不正确 2017-03-17'
        else:
            if len(args) == 3 and args[2] == 'frozen':
                calc_fxsys_data.update_all_liveness(today_datetime, True)
                calc_fxsys_data.calc_frozen_rebate()
                print 'frozen success'
            elif len(args) == 3 and args[2] == 'rebate':
                calc_fxsys_data.all_user_static_rebate(today_datetime)
                calc_fxsys_data.update_all_liveness(today_datetime)
                print 'rebate success'
            elif len(args) == 3 and args[2] == 'onlyrebate':
                calc_fxsys_data.all_user_static_rebate(today_datetime)
                print 'rebate success'
    else:
        calc_fxsys_data.check_all_profit()
        print 'check success'
    # today_datetime = datetime.datetime.strptime("2017-04-17 18:00:00", "%Y-%m-%d %H:%M:%S")
    # calc_fxsys_data.update_all_liveness(today_datetime,True)
