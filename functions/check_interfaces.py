import psutil

def listar_interfaces_fisicas():
    """
    Lista as interfaces de rede físicas no sistema operacional.

    :return: Lista de interfaces físicas
    """
    interfaces = psutil.net_if_addrs()
    # Filtrar apenas interfaces com endereços MAC (normalmente são físicas)
    interfaces_fisicas = [
        interface for interface, enderecos in interfaces.items()
        if any(addr.family == psutil.AF_LINK for addr in enderecos)
    ]
    return interfaces_fisicas