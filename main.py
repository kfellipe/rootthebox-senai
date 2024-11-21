from jinja2 import Environment, FileSystemLoader
import os, yaml, subprocess, apt

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

# Função para criar os containers do CTF
def create_CTF(single):
    for x in range(1,numero_jogadores+1):
    # Criando o arquivo de interfaces para adicionar uma interface para cada CTF criado
        number = f"{x:02}"
        with open(f"{interfaces_folder}/interface-ctf-{number}.conf", "w") as arq:
            arq.write(f"""
auto {interface_name}:1{number}
iface {interface_name}:1{number} inet static
    address {network}1{number}/24

    """)
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

def main():
    os.system("clear")
    print("\n\n", "=-" * 10, " Bem Vindo ", "=-" * 10, "\n\n")
    print(""" - Bem vindo ao script para criar um jogo CTF completo e de facil uso.
 - Para o correto funcionamento do script, é necessário seguir os passos
 - fornecidos no README.md e durante o processo de execução do mesmo.\n""")

    print("=" * 40)

    package_list = ['python3-yaml', 'python3-jinja2', 'pandoc', 'lynx']

    print("\nVerificando se os pacotes requeridos estão instalados: \n")

    for package in package_list:
        cache = apt.Cache()
        if cache[package].is_installed:
            print(f" -> {package} : Instalado")
        else:
            print(f" -> {package} : Não Instalado")

    with open("compose.yaml", "w") as arq:
        arq.write("")
    print("")
    print("=" * 40)
    print("\n--> Arquivo 'compose.yaml' limpo!\n")

    confirm = ""
    while confirm not in ["Yes", "yes", "y", "Y", "No", "no", "n", "N"]:
        print("=" * 40)
        print(f"""\n--> As seguintes configurações estão definidas atualmente no script:
            
 - Numero de jogadores: {numero_jogadores}
 - Diretorio de interfaces do sistema operacional: {interfaces_folder}
 - Rede dos containers: {network}
 - Diretorio de templates(leia o README): {web_files_folder}
 - Nome da interface física: {interface_name}
 - Imagem do docker: {docker_image}
 - Portas a serem publicadas(lista): {portas}""")
        confirm = str(input("\nDeseja prosseguir na execução?(Yes, No) "))
    if confirm in ["No", "no", "n","N"]:
        print("\nAté Logo!")
        exit()
    escolha = ""
    while escolha not in [1,2,3]:
        print("\n", "=" * 40)
        print("\nO que deseja instalar?\n1 - Containers CTF(arquivo docker compose)\n2 - RootTheBox\n3 - Ambos\n")
        escolha = int(input("Escolha entre as opções 1, 2 ou 3: "))
    
    composer = {}

    match escolha:
        case 1:
            composer['services'] = create_CTF(True)
        case 2:
            composer['services'] = create_rtb(True)
        case 3:
            composer['services'] = create_CTF(False) | create_rtb()

    with open("compose.yaml", "w") as arq:
        yaml.dump(composer, arq)

if __name__ == "__main__":
    main()
