#!/bin/bash

# Nome da imagem do container. Exemplo: "ubuntu:latest"
IMAGEM_DO_CONTAINER="nycolases6/ubuntu-bind9-nginx-ssh:1.0"

# Defina as portas que o container ira usar
# Exemplo: [22, 80, 443, 53]
PORTAS_DO_CONTAINER="80, 22, 53"

sudo yum update
sudo mkdir /data
sudo yum install docker python3-psutil python3-pip python3-yaml python3-jinja2 git -y

sudo python3 -m pip install rich

sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo git clone https://github.com/kfellipe/rootthebox-senai.git /data/rootthebox-senai

sudo cat <<EOF>/etc/systemd/system/start-ctf.service

[Unit]
Description=Serviço para iniciar container do CTF
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/bin/bash /data/rootthebox-senai/start-container-AWS.sh

[Install]
WantedBy=multi-user.targe

EOF

sudo python3 /data/rootthebox-senai/main.py "True" $IMAGEM_DO_CONTAINER $PORTAS_DO_CONTAINER

sudo systemctl daemon-reload

sudo systemctl start start-ctf

sudo systemctl enable start-ctf
