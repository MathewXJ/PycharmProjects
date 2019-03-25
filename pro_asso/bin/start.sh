#!/bin/bash

# Usage: start.sh

cd $(dirname "$0")

echo "starting pro_asso service ..."

# kill old run_txt_classification process
process_id=$(ps -ef | grep gunicorn | grep 'run_pro_asso:webapp' | awk '{ print $2 }' | tr '\n' ' ')
if [ "x${process_id}" != "x" ]; then
	kill -9 $process_id
	echo "process: $process_id killed."
fi

# start run_txt_classification process
nohup gunicorn -k sync -c gun_basic.conf run_pro_asso:webapp >/dev/null 2>&1 &

echo "starting pro_asso service success!"
