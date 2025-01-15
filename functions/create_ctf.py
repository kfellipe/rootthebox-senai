
# Função para criar os containers do CTF

import os
import subprocess

from functions.create_interfaces import create_interfaces

from rich.console import Console

console = Console(width=40)

def create_CTF(configs, aws):
    # Criando o arquivo de interfaces para adicionar uma interface para cada CTF criado
    if aws == False:
        while True:
            standalone = str(input("Criar CTF em modo standalone?[yes, no] ")).upper()
            if standalone in ['YES','Y']:
                configs['numero_jogadores'] = 1
                break
            if standalone in ['NO','N']:
                create_interfaces(players=configs['numero_jogadores'],interface=configs['interface_name'], file=f"{configs['interfaces_folder']}/ctf-interfaces.conf", network=configs['network'])
                my_cmd = "sudo systemctl restart networking"
                proc = subprocess.Popen(my_cmd, shell=True, stdout=subprocess.PIPE)
                break
            console.print(f"Apenas valores 'yes', 'y', 'n' ou 'no' são aceitos")
    else:
        standalone = "YES"
        configs['numero_jogadores'] = 1

    # Criando arquivo dos containers (composer)
    composer = {}
    for number in range(1,configs['numero_jogadores']+1):

        portas_container = []
        for porta in configs['portas']:
            if standalone not in ["YES","Y"]:
                portas_container.append(f"{configs['network']}{number}:{porta}:{porta}")
            else:
                portas_container.append(f"{porta}:{porta}")

        composer[f"ctf-{number}"] = {'image': configs['docker_image'], 
                                                'ports': portas_container,
                                                "container_name": f"CTF-{number}--web"}

    if standalone in ["NO", "N"]:
        with open("mapeamento_de_ip.md", "w") as arq:
            arq.write("# Mapeamento de IP\n")
            arq.write("<table><tr><th>Jogador</th><th>Endereço IP</th></tr>")
            for number in range(1, configs['numero_jogadores']+1):
                arq.write(f"<tr><td>{number}</td><td>{configs['network']}{number}</td></tr>")
            arq.write("</table>")

    return composer