# Função para criar o arquivo das interfaces

def create_interfaces(players, file, interface, network):
    with open(file, "w") as arq:
        arq.write("")
    for x in range(1, players+1):
        with open(file,"a") as arq:
            arq.write(f"""
auto {interface}:{x}
iface {interface}:{x} inet static
    address {network}{x}
    netmask 255.255.255.0

""")