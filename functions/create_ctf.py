
# Função para criar os containers do CTF

import os
import subprocess

from jinja2 import Environment, FileSystemLoader
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
    if configs['web_files_folder'] != "":
        try:
            os.mkdir(configs['web_files_folder'])
        except PermissionError:
            print(f"Permission denied: Unable to create '{configs['web_files_folder']}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        pwd = os.path.dirname(os.path.abspath(__file__))
        for number in range(1,configs['numero_jogadores']+1):
        # Criando uma pasta para cada CTF criado e copia os arquivos da pasta template para cada uma
            directory_name=f"{configs['web_files_folder']}/ctf-{number}"
            try:
                os.mkdir(directory_name)
                print(f"Directory '{directory_name}' created successfully.")
            except FileExistsError:
                print(f"Directory '{directory_name}' already exists.")
            except PermissionError:
                print(f"Permission denied: Unable to create '{directory_name}'.")
            except Exception as e:
                print(f"An error occurred: {e}")
            os.system(f"cp {pwd}/../template/* {directory_name} -r")

    # Criando arquivo dos containers (composer)
    composer = {}
    for number in range(1,configs['numero_jogadores']+1):

        portas_container = []
        for porta in configs['portas']:
            if standalone not in ["YES","Y"]:
                portas_container.append(f"{configs['network']}{number}:{porta}:{porta}")
            else:
                portas_container.append(f"{porta}:{porta}")

        if configs['web_files_folder'] != "":
            composer[f"ctf-{number}"] = {'image': configs['docker_image'], 
                                                    'ports': portas_container, 
                                                    "volumes": [f"{pwd}/{configs['web_files_folder']}/ctf-{number}:/var/www/html"],
                                                    "container_name": f"CTF-{number}--web"}
        else:
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