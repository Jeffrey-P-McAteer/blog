#!/bin/sh

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$DIR"

gcloud compute ssh ftp -- 'sudo mkdir -p /opt/jftp/ ; sudo mkdir -p /opt/jftp/data/ ; sudo chown -R $(whoami) /opt/jftp/'
gcloud compute scp "jftp.py" ftp:/opt/jftp/jftp.py
gcloud compute scp "jftp.service" ftp:/tmp/jftp.service
gcloud compute ssh ftp -- 'sudo mv /tmp/jftp.service /etc/systemd/system/jftp.service'
gcloud compute ssh ftp -- 'sudo systemctl enable --now jftp ; sudo systemctl restart jftp'

# Other deployment one-time commands:
# sudo pacman -S python python-pip
# sudo python3 -m pip install pyftpdlib

