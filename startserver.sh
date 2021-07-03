#!/bin/bash

# this is a script to start a locally hosted test server for a given site using WSL

my_ip=`ifconfig | awk 'FNR == 2 {print $2}'`
errormsg="Unknown or invalid options. See below\n --port=<port_number>  (If unspecified, defaults to 8001)"
PORT=8001
for i in "$@"
do
	case $i in
		--port=*)
			PORT=${i#*=}
			;;
		*)
		echo -e $errormsg
		exit
	esac
done

echo -e "Webserver hosted at $my_ip:$PORT"
source ./.venv/bin/activate && python manage.py runserver 0.0.0.0:$PORT --settings config.settings.development