#!/bin/bash

# Nome da imagem do container. Exemplo: "ubuntu:latest"
IMAGEM_DO_CONTAINER="nycolases6/ubuntu-bind9-nginx-ssh:1.1"

# Se desejar instalar o RootTheBox junto ao jogo, mude a opção abaixo para "True"
ROOTTHEBOX="False"

# Defina as portas que o container ira usar
# Exemplo: "22,80,443,53"
PORTAS_DO_CONTAINER="80,22"

sudo echo "Port 2022" >> /etc/ssh/sshd_config

sudo systemctl restart sshd

sudo apt update

sudo mkdir /data

sudo apt install docker docker-compose python3-psutil python3-pip python3-yaml python3-jinja2 python3-apt git -y

sudo python3 -m pip install rich

sudo git clone https://github.com/kfellipe/rootthebox-senai.git /data/rootthebox-senai

sudo cat <<EOF>/etc/systemd/system/start-ctf.service

[Unit]
Description=Serviço para iniciar container do CTF
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/bin/bash /data/rootthebox-senai/start-container-AWS.sh

[Install]
WantedBy=multi-user.target

EOF

sudo python3 /data/rootthebox-senai/main.py "True" $ROOTTHEBOX $IMAGEM_DO_CONTAINER $PORTAS_DO_CONTAINER

sudo systemctl daemon-reload

sudo systemctl start start-ctf

sudo systemctl enable start-ctf