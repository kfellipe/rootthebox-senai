from jinja2 import Environment, FileSystemLoader, Template
import os, yaml, subprocess, time
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from functions.create_ctf import create_CTF
from functions.create_rtb import create_rtb
from functions.check_and_install_package import check_and_install_package

# Edite essas variaveis de acordo com o seu uso
# Maximo de 154(incluindo)
configs = {
    "numero_jogadores": 10,
    "interfaces_folder": "/etc/network/interfaces.d",
    "web_files_folder": "",
    "interface_name": "ens224",
    "network": "10.1.1.",
    "docker_image": "nycolases6/ubuntu-bind9-nginx-ssh:1.0",
    "portas": ["80", "22", "53"]
}

def limpar_tela():
    os.system("clear")

def main():
    limpar_tela()
    console = Console(width=40)
    console.print("Bem Vindo!", style="bold italic cyan on white", justify="center")
    console.print("Bem vindo ao script para criar um jogo CTF completo e de facil uso. Para o correto funcionamento do script, é necessário seguir os passos fornecidos no README.md e durante o processo de execução do mesmo.", style="white on black", overflow="fold", justify="left")

    print("\n" + "=" * 40 + "\n")

    package_list = ['python3-yaml', 'python3-jinja2', 'pandoc', 'lynx']

    console.print("Verificando se os pacotes requeridos estão instalados:", style="white on black", justify="center")

    for package in package_list:
        check_and_install_package(package)

    with open("compose.yaml", "w") as arq:
        arq.write("")
    print("")
    print("=" * 40)
    console.print("\nArquivo 'compose.yaml' limpo!\n", style="white on black")

    confirm = ""
    while True:
        print("=" * 40)
        table1 = Table(width=40, title="As seguintes configurações estão definidas atualmente no script")
        table1.add_column("Configuração", style="cyan on black", overflow="fold")
        table1.add_column("Configurado como", style="white on black")
        table1.add_row("Numero de jogadores\n", str(configs['numero_jogadores']))
        table1.add_row("Diretorio de interfaces\n", str(configs['interfaces_folder']))
        table1.add_row("Rede dos containers\n", str(configs['network']))
        table1.add_row("Diretorio de templates\n", str(configs['web_files_folder']))
        table1.add_row("Nome da interface física\n", str(configs['interface_name']))
        table1.add_row("Imagem do docker\n", str(configs['docker_image']))
        table1.add_row("Portas a serem publicadas", str(configs['portas']))
        console.print(table1)
        confirm = str(input("\nDeseja prosseguir na execução?(Yes, No) ")).upper()
        if confirm in ["NO", "N"]:
            print("\nAté Logo!")
            exit()
        if confirm in ["YES", "Y"]:
            break
    escolha = ""
    while escolha not in [1,2,3]:
        print("\n", "=" * 40)
        print("\nO que deseja instalar?\n1 - Containers CTF(arquivo docker compose)\n2 - RootTheBox\n3 - Ambos\n")
        escolha = int(input("Escolha entre as opções 1, 2 ou 3: "))
    
    composer = {}

    match escolha:
        case 1:
            composer['services'] = create_CTF(configs=configs)
        case 2:
            composer['services'] = create_rtb()
        case 3:
            composer['services'] = create_CTF(configs=configs) | create_rtb()

    with open("compose.yaml", "w") as arq:
        yaml.dump(composer, arq)

if __name__ == "__main__":
    main()
