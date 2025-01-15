from rich.console import Console
from rich.table import Table
import os, docker
from functions.check_interfaces import listar_interfaces_fisicas
from functions.check_docker_image import verificar_e_baixar_imagem

# "numero_jogadores": 10,
# "interfaces_folder": "/etc/network/interfaces.d",
# "web_files_folder": "",
# "interface_name": "ens224",
# "network": "10.1.1.",
# "docker_image": "nycolases6/ubuntu-bind9-nginx-ssh:1.0",
# "portas": ["80", "22", "53"]

def verify_options(minimo, maximo):
    console = Console(width=40)
    try:
        valor = int(input(f"Escolha um valor entre {minimo} e {maximo}: "))
        if valor < minimo or valor > maximo:
            limpar_tela()
            console.print(f"Apenas valores entre {minimo} e {maximo} são aceitos!", style="bold white on red", justify="center")
            return False
        else:
            return valor
    except:
        limpar_tela()
        console.print("Valor invalido!", style="bold white on red", justify="center")
        return False

def limpar_tela():
    os.system("clear")

def change_configs(configs):
    console = Console(width=40)
    confirm = 0
    limpar_tela()
    while True:
        table = Table(width=40, title="Escolha uma das configurações para mudar", title_style="cyan on black", title_justify="center")
        table.add_column("Item", style="green on black")
        table.add_column("Configuração", style="white on black")
        table.add_column("Valor", style="orange1 on black")
        count = 0
        for config in configs:
            count += 1
            table.add_row(str(count), str(config), f"{str(configs[config])}\n")
        table.add_row("8", "sair")
        console.print(table)
        confirm = verify_options(1, 8)

        if confirm == 1:
            limpar_tela()
            while True:
                console.print(f"Numero de jogadores, atualmente configurado: {configs['numero_jogadores']}", justify="center", style="white on black")
                choice = verify_options(1, 150)
                if choice != False:
                    configs["numero_jogadores"] = choice
                    limpar_tela()
                    break
        if confirm == 2:
            limpar_tela()
            console.print(f"Diretorio das interfaces de rede, atualmente configurado: {configs['interfaces_folder']}", justify="center", style="white on black")
            choice = str(input("Diretorio[/etc/network/interfaces.d]: "))
            if choice == "":
                configs["interfaces_folder"] = "/etc/network/interfaces.d"
            else:
                configs["interfaces_folder"] = choice
            limpar_tela()
            break
        if confirm == 3:
            limpar_tela()
            while True:
                console.print(f"Diretorio dos arquivos html, atualmente configurado: {configs['web_files_folder']}", justify="center", style="white on black")
                console.print(f"Escolha uma das opções abaixo:", justify="center", style="white on black")
                table = Table(width=40)
                table.add_column("Item", style="cyan on black")
                table.add_column("Opção", style="orange1 on black")
                table.add_row("1", "")
                table.add_row("2", "html_files")
                table.add_row("3", "web_files")
                console.print(table)
                choice = verify_options(1,4)
                if choice != False:
                    match choice:
                        case 1:
                            configs["web_files_folder"] = ""
                        case 2:
                            configs["web_files_folder"] = "html_files"
                        case 3:
                            configs["web_files_folder"] = "web_files"
                    limpar_tela()
                    break
        if confirm == 4:
            limpar_tela()
            while True:
                table = Table(width=40, title="Escolha uma das configurações para mudar", title_style="cyan on black", title_justify="center")
                table.add_column("Item", style="green on black")
                table.add_column("Interface", style="white on black")
                interfaces = listar_interfaces_fisicas()
                item = 0
                for interface in interfaces:
                    item += 1
                    table.add_row(f"{item}",f"{interface}\n")
                console.print(table)
                choice = verify_options(1, item)
                if choice != False:
                    configs['interface_name'] = interfaces[choice-1]
                    break
        if confirm == 5:
            limpar_tela()
            while True:
                networks = ["10.1.1.", "172.10.0.", "192.168.254."]
                table = Table(width=40, title="Escolha uma das configurações para mudar", title_style="cyan on black", title_justify="center")
                table.add_column("Item", style="green on black")
                table.add_column("Rede", style="white on black")
                item = 0
                for network in networks:
                    item += 1
                    table.add_row(f"{item}", f"{network}")
                console.print(table)
                choice = verify_options(1, 3)
                if choice != False:
                    configs['network'] = networks[choice-1]
                    break
        if confirm == 6:
            limpar_tela()
            while True:
                console.print(f"Atualmente configurado como: {configs['docker_image']}", style="white on black")
                nome_imagem = str(input("Digite o nome da imagem Docker (exemplo: 'ubuntu:latest'): "))
                try:
                    # Conecta ao daemon do Docker
                    cliente_docker = docker.from_env()

                    # Verifica se a imagem existe localmente
                    try:
                        cliente_docker.images.get(nome_imagem)
                        console.print(f"A imagem '{nome_imagem}' existe localmente.", style="white on black")
                        configs['docker_image'] = nome_imagem
                        limpar_tela()
                        break
                    except docker.errors.ImageNotFound:
                        console.print(f"A imagem '{nome_imagem}' não foi encontrada localmente. Fazendo download...", style="white on black")
                        cliente_docker.images.pull(nome_imagem)
                        console.print(f"Download da imagem '{nome_imagem}' concluído com sucesso!", style="white on black")
                        configs['docker_image'] = nome_imagem
                        limpar_tela()
                        break
                    except docker.errors.APIError as e:
                        limpar_tela()
                        console.print(f"Erro ao verificar ou baixar a imagem: {e}", style="bold white on red")
                except docker.errors.DockerException as e:
                    limpar_tela()
                    console.print(f"Erro ao conectar ao Docker: {e}", style="bold white on red")
        if confirm == 7:
            portas = []
            limpar_tela()
            while True:
                console = Console(width=40)
                console.print(f"Configurando as portas a serem publicadas", style="white on black")
                console.print(f"Portas: {portas}")
                console.print(f"Digite zero para sair")
                choice = verify_options(0,1024)
                if choice != False:
                    if choice not in portas:
                        limpar_tela()
                        portas.append(choice)
                        console.print(f"Porta adicionada!", style="green on black")
                    else:
                        limpar_tela()
                        console.print(f"Porta ja existe!", style="white on red")
                if choice == 0:
                    limpar_tela()
                    configs['portas'] = portas
                    break
        if confirm == 8:
            limpar_tela()
            break