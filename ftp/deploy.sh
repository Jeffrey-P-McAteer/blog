#!/bin/sh

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$DIR"

# yay -S doctl
# doctl auth init
# https://developers.digitalocean.com/documentation/v2/

deploy_new_vm() {
  doctl compute droplet create 'ftp' \
    --region 'nyc3' \
    --image 'centos-8-x64' \
    --size 's-1vcpu-1gb'
  # pK-Bngca69
}

doctl_ssh() {
  doctl compute ssh --ssh-key-path '/j/i/doctl_id' root@ftp --ssh-command "$1"
}

setup_os() {
  doctl_ssh 'sudo dnf install -y python3 python3-pip ; sudo python3 -m pip install pyftpdlib'
  doctl_ssh 'sudo mkdir -p /opt/jftp/ ; sudo mkdir -p /opt/jftp/data/ ; sudo chown -R $(whoami) /opt/jftp/'
}

copy_files() {
  # gcloud compute scp "jftp.py" ftp:/opt/jftp/jftp.py
  # gcloud compute scp "jftp.service" ftp:/tmp/jftp.service
  doctl_ssh 'cat > /opt/jftp/jftp.py' < jftp.py
  doctl_ssh 'cat > /tmp/jftp.service' < jftp.service
}

restart_services() {
  doctl_ssh 'sudo mv /tmp/jftp.service /etc/systemd/system/jftp.service'
  doctl_ssh 'sudo systemctl enable --now jftp ; sudo systemctl restart jftp'
}

# perform work

#deploy_new_vm
#setup_os
copy_files
restart_services

