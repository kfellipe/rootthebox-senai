
# Função para criar os containers do CTF

import os
import subprocess

from jinja2 import Environment, FileSystemLoader
from functions.create_interfaces import create_interfaces


def create_CTF(configs):
    # Criando o arquivo de interfaces para adicionar uma interface para cada CTF criado
    create_interfaces(players=configs['numero_jogadores'],interface=configs['interface_name'], file=f"{configs['interfaces_folder']}/ctf-interfaces.conf", network=configs['network'])
    my_cmd = "sudo systemctl restart networking"
    proc = subprocess.Popen(my_cmd, shell=True, stdout=subprocess.PIPE)
    if configs['web_files_folder'] != "":
        try:
            os.mkdir(configs['web_files_folder'])
            print(f"Directory '{configs['web_files_folder']}' created successfully.")
        except FileExistsError:
            print(f"Directory '{configs['web_files_folder']}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{configs['web_files_folder']}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        pwd = os.path.abspath(os.getcwd())
        environment = Environment(loader=FileSystemLoader("templates/"))
        template = environment.get_template("index.html")
        for x in range(1,configs['numero_jogadores']+1):
        # Criando uma pasta e um arquivo template para cada CTF criado
            content = template.render(number=number)
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
            with open(f"{configs['web_files_folder']}/ctf-{number}/index.html", mode="w", encoding="utf-8") as arq:
                arq.write(content)

    # Criando arquivo dos containers (composer)
    composer = {}
    for number in range(1,configs['numero_jogadores']+1):

        portas_container = []
        for porta in configs['portas']:
            portas_container.append(f"{configs['network']}{number}:{porta}:{porta}")

        if configs['web_files_folder'] != "":
            composer[f"ctf-{number}"] = {'image': configs['docker_image'], 
                                                    'ports': portas_container, 
                                                    "volumes": [f"{pwd}/{configs['web_files_folder']}/ctf-{number}:/usr/share/nginx/html"],
                                                    "container_name": f"CTF-{number}--web"}
        else:
            composer[f"ctf-{number}"] = {'image': configs['docker_image'], 
                                                    'ports': portas_container,
                                                    "container_name": f"CTF-{number}--web"}

    with open("mapeamento_de_ip.md", "w") as arq:
        arq.write("# Mapeamento de IP\n")
        arq.write("<table><tr><th>Jogador</th><th>Endereço IP</th></tr>")
        for number in range(1, configs['numero_jogadores']+1):
            arq.write(f"<tr><td>{number}</td><td>{configs['network']}{number}</td></tr>")
        arq.write("</table>")

    return composer