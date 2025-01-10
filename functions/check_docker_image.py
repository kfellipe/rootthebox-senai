import docker
from rich.console import Console

console = Console

def verificar_e_baixar_imagem(nome_imagem):
    """
    Verifica se uma imagem Docker existe localmente e faz o download se não existir.

    :param nome_imagem: Nome completo da imagem (exemplo: 'ubuntu:latest')
    """
    try:
        # Conecta ao daemon do Docker
        cliente_docker = docker.from_env()

        # Verifica se a imagem existe localmente
        try:
            cliente_docker.images.get(nome_imagem)
            console.print(f"A imagem '{nome_imagem}' já existe localmente.", style="white on black")
            return nome_imagem
        except docker.errors.ImageNotFound:
            console.print(f"A imagem '{nome_imagem}' não foi encontrada localmente. Fazendo download...", style="white on black")
            cliente_docker.images.pull(nome_imagem)
            console.print(f"Download da imagem '{nome_imagem}' concluído com sucesso!", style="white on black")
            return nome_imagem
        except docker.errors.APIError as e:
            console.print(f"Erro ao verificar ou baixar a imagem: {e}", style="bold white on red")
            return False
    except docker.errors.DockerException as e:
        console.print(f"Erro ao conectar ao Docker: {e}", style="bold white on red")
        return False