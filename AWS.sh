#!/bin/bash

# Nome da imagem do container. Exemplo: "ubuntu:latest"
IMAGEM_DO_CONTAINER="nycolases6/ubuntu-bind9-nginx-ssh:1.0"

# Defina as portas que o container ira usar
# Exemplo: [22, 80, 443, 53]
PORTAS_DO_CONTAINER="[80, 22, 53]"

sudo apt update

sudo apt install docker docker-compose python3-psutil git -y

sudo mkdir /data -p

sudo cd /data

sudo git clone https://github.com/kfellipe/rootthebox-senai.git

sudo cd /data/rootthebox-senai

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

sudo systemctl daemon-reload

sudo systemctl start start-ctf

sudo systemctl enable start-ctf

sudo python3 main.py "True" $IMAGEM_DO_CONTAINER $PORTAS_DO_CONTAINER