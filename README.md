# RootTheBox SENAI
## Bem-vindo ao script para criar um jogo CTF utilizando containers docker

### Instalando em um ambiente AWS
Para a correta instalação utilizando um ambiente AWS, siga os seguintes passos:<br>
Crie uma instância EC2:
 - Utilize Debian como sistema operacional.
 - Edite "Número de instâncias" para o numero de jogadores.
 - Adicione uma nova regra de segurança para permitir qualquer IP realizar requisições na porta 2022.
 - Permita o tráfego HTTP.
 - Entre nesse [link](https://raw.githubusercontent.com/kfellipe/rootthebox-senai/refs/heads/master/AWS.sh) e copie todo o conteudo da pagina.<br>
Cole o conteudo no campo "dados de usuário" (em "detalhes avançados").

Após seguir esses passos, execute a instância e aguarde a instância ligar e o script executar. (~6min)

Agora, basta acessar seu container através do IP público da sua instância.

### Instalando em um ambiente onprimise

#### Observações
 - O script foi criado e testado em um ambiente com sistema operacional debian 12(bookworm).
 - Certifique-se de estar logado no super-usuário(root) para o correto funcionamento do script.
 - Execute o comando:<br> <code> sudo -l </code> <br>e veja se o comando existe, caso não exista, execute:<br> <code> apt update </code><br><code> apt install sudo -y </code><br>
e tente executar o comando novamente. <br>

#### Instalando as dependências
 - Instale as dependências necessárias usando o seguinte comando: <br> <code> sudo apt install docker docker-compose python3-psutil python3-pip python3-yaml python3-apt python3-rich pandoc lynx git -y </code>
 - Execute o comando:<br> <code> git clone https://github.com/kfellipe/rootthebox-senai.git </code>

#### Executando o script
 - Entre na pasta com o comando: <code> cd rootthebox-senai </code> e execute o comando <code> python3 main.py </code>
 - Será apresentado as configurações padrão do script como: numero de jogadores, imagem do docker, etc... Se você concorda com as configurações, escreva "yes" e aperte "Enter".
 - Se desejar editar alguma configuração, digite "edit" e pressione "Enter".
 - Você terá que decidir se deseja instalar apenas os containers(opção 1), apenas o rootthebox(opção 2) ou ambos(opção 3).
 - Se você optar por instalar apenas os containers(opção 1) ou ambos(opção 3), você precisará decidir entre usar o modo standalone ou não.
 - Modo Standalone: vai configurar apenas um container docker e esse container irá utilizar o endereço IP do host.(ideal para atividades individuais)
 - Execute o comando: <br>
<code> docker-compose up -d </code>
 - Para saber como acessar os containers, o script criará um arquivo chamado "mapeamento_de_ip.md", execute o comando: <br><code> pandoc mapeamento_de_ip.md | lynx -stdin </code>
 - Para acessar o RootTheBox(caso você opte por inicia-lo também), basta usar o endereço IP da sua máquina host com a porta 8888 em um navegador.