#!/usr/bin/env bash

pkill -f 8000
cd ..
svn update
python manage.py runserver 0.0.0.0:8000 &

pkill -f tornado_per
python tornado_per_1m.py &
python tornado_per_3m.py &
python tornado_per_30m.py &
python tornado_per_3s.py &
python tornado_per_1m_lps3.py &