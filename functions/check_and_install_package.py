import apt

def check_and_install_package(package_name):
    """
    Verifica se um pacote está instalado e, caso não esteja, instala-o
    com uma barra de progresso para a instalação.
    """
    # Cria um cache do APT
    cache = apt.Cache()
    cache.update()  # Atualiza o cache do APT
    cache.open()

    if package_name in cache:
        package = cache[package_name]
        if package.is_installed:
            print(f"[✔] O pacote '{package_name}' já está instalado.")
        else:
            print(f"[✘] O pacote '{package_name}' não está instalado. Iniciando a instalação...")
            # Exibe uma barra de progresso durante a instalação
            with Progress() as progress:
                task = progress.add_task("[cyan]Instalando o pacote...", total=100)

                try:
                    # Simula a instalação com barra de progresso
                    process = subprocess.Popen(
                        ["sudo", "apt", "install", "-y", package_name],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    while process.poll() is None:
                        progress.update(task, advance=5)
                        time.sleep(0.5)  # Simula o progresso
                    # Conclui o progresso quando a instalação terminar
                    progress.update(task, advance=100 - progress.tasks[0].completed)
                    
                    # Verifica o status do processo
                    if process.returncode == 0:
                        print(f"[✔] O pacote '{package_name}' foi instalado com sucesso.")
                    else:
                        print(f"[✘] Falha ao instalar o pacote '{package_name}'.")
                except Exception as e:
                    print(f"[✘] Erro durante a instalação: {e}")
    else:
        print(f"[✘] O pacote '{package_name}' não foi encontrado nos repositórios configurados.")