# RootTheBox SENAI
## Bem-vindo ao script para criar um jogo CTF utilizando containers docker

## Instalando em um ambiente AWS
Para a correta instalação utilizando um ambiente AWS, siga os seguintes passos:<br>
Crie uma instância EC2


### Observações importantes
O script foi criado e testado em um ambiente com sistema operacional debian 12(bookworm). <br> 
Certifique-se de estar logado no super-usuário(root) para o correto funcionamento do script. <br>
Execute o comando:<br> <code> sudo -l </code> <br>e veja se o comando existe, caso não exista, execute:<br> <code> apt update </code><br><code> apt install sudo -y </code><br>
e tente executar o comando novamente.
Execute o comando:<br> <code> systemctl status networking </code>

<hr>

### Instalando as dependências necessárias
Primeiro passo, precisamos criar um Ambiente Virtual em python(venv) usando o seguinte comando: <code>python3 -m venv .venv</code>.<br><br>
Agora, precisamos ativar a venv com o seguinte comando: <code>source .venv/bin/activate</code>.<br><br>
Instale as dependencias necessarias <code>pip install pyyaml jinja2 psutil </code>.<br><br>
Após a instalação, execute o comando <code>python3 main.py</code>.<br><br>
Será pedido para você escolher uma das três opções de instalação: Instalar somente o RootTheBox, instalar somente os containers CTF ou instalar o RootTheBox e os containers CTF.<br><br>
Esse comando, irá criar os arquivos de configurações de cada interface para cada jogador dentro do diretório especificado no script(padrão "/etc/network/interfaces.d/"), vai ligar cada interface criada, e vai criar o arquivo compose.yaml responsável por ligar os containers de cada jogador.<br><br>
Se for passado a variavel "web_files_folder", você terá que criar uma pasta chamada "templates" e criar um arquivo dentro chamado index.html, esse arquivo será replicado para cada container dos jogadores(o arquivo tem que ser escrito em jinja2).<br><br>
Após a execução completa do script, execute o seguinte comando para iniciar os containers: <code>docker compose up</code>.<br><br>
Para saber as informações sobre cada container e cada endereço IP, verifique o arquivo "mapeamento_de_ip.md" com o comando <code>pandoc mapeamento_de_ip.md | lynx -stdin </code>.