# Projeto_Compra_De_Moedas
Este repositório contém o conteúdo do projeto de compra de Moedas usando o DJango(python).

___

## First Steps: 

Para iniciar o projeto em sua máquina tenha o Python instalado e o MySql Server (localmente ou remotamente).

Baixe ou clone esse repositorio onde achar melhor.

Para começar a usar acesse o repositório por meio do cmd ou prompt de comando do seu sistema.

Inicie uma VM do python (máquina virtual) (comando)-> python -m venv venv

Navegue até "venv/scripts" e digite o comando "activate"

Com a máquina virtual ativada volte até a raiz do projeto e digite o (comando) -> pip install -r requirements.txt

Após instalar todas as dependencias do projeto será necessário criar as tabelas.

Criar Migrations do app de usuarios (comando) -> py manage.py makemigrations usuarios
Criar tabelas de usuarios (comando) -> py manage.py migrate

Criar Migrations do app core (comando) -> py manage.py makemigrations core
Criar tabelas do app core (comando) -> py manage.py migrate

### Após isso basta rodar o projeto (comando) -> py manage.py runserver 
O Projeto estará rodando no endereço "localhost:8000".
