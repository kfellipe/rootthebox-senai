from jinja2 import Environment, FileSystemLoader, Template
import os, yaml, subprocess, apt
from rich.console import Console
from rich.table import Table

# Edite essas variaveis de acordo com o seu uso
# Maximo de 154(incluindo)
numero_jogadores=30
interfaces_folder="/etc/network/interfaces.d"
# SOMENTE OS 3 PRIMEIROS DECIMAIS COM UM . NO FINAL
network="10.1.1."
web_files_folder=""
interface_name="ens224"
docker_image="nycolases6/ubuntu-bind9-nginx-ssh:1.0"
portas=["80", "22", "53"]

def limpar_tela():
    os.system("clear")

# Função para criar os containers do CTF
def create_CTF():
    for x in range(1,numero_jogadores+1):
    # Criando o arquivo de interfaces para adicionar uma interface para cada CTF criado
        number = f"{x:02}"
        template_str = """
{% for x in range(number) %}
auto {{interface_name}}:1{{x}}
iface {{interface_name}}:1{{x}} inet static
    address {{network}}1{{x}}/24
{% endfor %}
"""

        # Criar o template a partir da string
        template = Template(template_str)

        # Renderizar o template com os dados
        output = template.render(number=number)
        with open(f"{interfaces_folder}/interfaces-ctf.conf", "w") as arq:
            arq.write(output)
        my_cmd = f"sudo ifup {interface_name}:1{number}"
        proc = subprocess.Popen(my_cmd, shell=True, stdout=subprocess.PIPE)
    if web_files_folder != "":
        try:
            os.mkdir(web_files_folder)
            print(f"Directory '{web_files_folder}' created successfully.")
        except FileExistsError:
            print(f"Directory '{web_files_folder}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{web_files_folder}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        pwd = os.path.abspath(os.getcwd())
        environment = Environment(loader=FileSystemLoader("templates/"))
        template = environment.get_template("index.html")
        for x in range(1,numero_jogadores+1):
        # Criando uma pasta e um arquivo template para cada CTF criado
            content = template.render(number=number)
            directory_name=f"{web_files_folder}/ctf-{number}"
            try:
                os.mkdir(directory_name)
                print(f"Directory '{directory_name}' created successfully.")
            except FileExistsError:
                print(f"Directory '{directory_name}' already exists.")
            except PermissionError:
                print(f"Permission denied: Unable to create '{directory_name}'.")
            except Exception as e:
                print(f"An error occurred: {e}")
            with open(f"{web_files_folder}/ctf-{number}/index.html", mode="w", encoding="utf-8") as arq:
                arq.write(content)

    # Criando arquivo dos containers (composer)
    composer = {}
    for x in range(1,numero_jogadores+1):
        number = f"{x:02}"

        portas_container = []
        for porta in portas:
            portas_container.append(f"{network}1{number}:{porta}:{porta}")

        if web_files_folder != "":
            composer[f"ctf-{number}"] = {'image': docker_image, 
                                                    'ports': portas_container, 
                                                    "volumes": [f"{pwd}/{web_files_folder}/ctf-{number}:/usr/share/nginx/html"],
                                                    "container_name": f"CTF-{number}--web"}
        else:
            composer[f"ctf-{number}"] = {'image': docker_image, 
                                                    'ports': portas_container,
                                                    "container_name": f"CTF-{number}--web"}

    with open("mapeamento_de_ip.md", "w") as arq:
        arq.write("# Mapeamento de IP\n")
        arq.write("<table><tr><th>Jogador</th><th>Endereço IP</th></tr>")
        for x in range(1, numero_jogadores+1):
            number = f"{x:02}"
            arq.write(f"<tr><td>{number}</td><td>{network}1{number}</td></tr>")
        arq.write("</table>")

    return composer

def create_rtb():
    composer = {
        "memcached": {"image": "memcached:latest", "ports":['11211:11211']},
        "webapp":{"build":"./RootTheBox/", "ports":["8888:8888"], "volumes": ["./RootTheBox/files:/opt/rtb/files:rw"],"environment":["COMPOSE_CONVERT_WINDOWS_PATHS=1"]}}
    return composer

def is_package_installed(package_name):
    # Cria um cache do APT
    cache = apt.Cache()
    # Atualiza o cache (opcional, se você quer garantir os dados mais recentes)
    cache.update()
    cache.open()
    
    # Verifica se o pacote existe no cache
    if package_name in cache:
        package = cache[package_name]
        # Retorna True se o pacote está instalado
        return package.is_installed
    else:
        # O pacote não existe no cache
        return False

def main():
    limpar_tela()
    console = Console(width=40)
    console.print("Bem Vindo!", style="bold italic cyan on white", justify="center")
    console.print("Bem vindo ao script para criar um jogo CTF completo e de facil uso. Para o correto funcionamento do script, é necessário seguir os passos fornecidos no README.md e durante o processo de execução do mesmo.", style="white on black", overflow="fold", justify="left")

    print("\n" + "=" * 40 + "\n")

    package_list = ['python3-yaml', 'python3-jinja2', 'pandoc', 'lynx']

    console.print("Verificando se os pacotes requeridos estão instalados:", style="white on black", justify="center")

    table = Table(width=40)

    table.add_column("Pacote", style="cyan on black", overflow="fold")
    table.add_column("Instalado", style="white on black")
    for package in package_list:
        if is_package_installed(package):
            table.add_row(package, "SIM")
        else:
            table.add_row(package, "NÃO")

    console.print(table)

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
        table1.add_row("Numero de jogadores\n", str(numero_jogadores))
        table1.add_row("Diretorio de interfaces\n", str(interfaces_folder))
        table1.add_row("Rede dos containers\n", str(network))
        table1.add_row("Diretorio de templates\n", str(web_files_folder))
        table1.add_row("Nome da interface física\n", str(interface_name))
        table1.add_row("Imagem do docker\n", str(docker_image))
        table1.add_row("Portas a serem publicadas", str(portas))
        console.print(table1)
        confirm = str(input("\nDeseja prosseguir na execução?(Yes, No) "))
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
            composer['services'] = create_CTF()
        case 2:
            composer['services'] = create_rtb()
        case 3:
            composer['services'] = create_CTF() | create_rtb()

    with open("compose.yaml", "w") as arq:
        yaml.dump(composer, arq)

if __name__ == "__main__":
    main()
