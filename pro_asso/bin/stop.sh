#!/bin/bash

# Usage: stop.sh

cd $(dirname "$0")

echo "stopping pro_asso service ..."

# kill run_txt_classification process
process_id=$(ps -ef | grep gunicorn | grep 'run_pro_asso:webapp' | awk '{ print $2 }' | tr '\n' ' ')
kill -9 $process_id
echo "process: $process_id killed."

echo "stopping pro_asso success!"
