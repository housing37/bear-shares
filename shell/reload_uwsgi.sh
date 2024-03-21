#!/usr/bin/env bash
echo 'STARTING RELOAD UWSGI ...'

# print current system info
echo 'current filesystem data....'
df -h
echo 'current filesystem data.... DONE'
echo ''

# check / print current uwsgi running
echo 'current uwsgi running.... (3 logs = 1 instance; i think)'
ps aux | grep uwsgi
echo 'current uwsgi running.... DONE'
echo ''

# kill all uwsgi running
echo 'kill all running uwsgi running.... (and then sleep x)'
pkill -f uwsgi -9
sleep 2
echo 'kill all running uwsgi running.... DONE'
echo ''

# print current running (ensure all killed)
echo 're-check current uwsgi running.... (1 log = 0 instances)'
ps aux | grep uwsgi
echo 're-check current uwsgi running.... DONE'
echo ''

# re-launch uwsgi instances (x2)
echo 'start running list of all UWSGIs....'
sudo uwsgi --enable-threads --ini /srv/www/gms_post/src/deploy.ini
echo 'start running list of all UWSGIs.... 1) gms_post DONE'
echo ''
sudo uwsgi --enable-threads --ini /srv/www/gms_serv_gasp/src/deploy.ini
echo 'start running list of all UWSGIs.... 2) gms_serv_gasp DONE'
echo ''
echo 'start running list of all UWSGIs.... ALL DONE'
echo ''


