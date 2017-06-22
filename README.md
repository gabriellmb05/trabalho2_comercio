# trabalho2_comercio

## Instalação

Todo o processo de instalação e configuração será feito em um ambiente linux.

### Pré Requisitos

* python >= 2.7
* virtualenv

### Configuração

Execute o comando para possibilitar a configuração da biblioteca psycopg2:

  sudo apt-get install python3-dev python-dev
  
Em seguida crie e ative o ambiente virtual com os comandos:

  virtualenv -p python3 env
  source env/bin/activate

Instale as bibliotecas com o comando:

  pip install -r requirements.txt
  
 Certifique-se de que o banco "moviedb" foi criado em sua base postgres conforme explicado na seção "Modelo Conceitual" na wiki.
 
 Para rodar o projeto execute o comando:
 
  python3 manage.py runserver
  
  Para acessar o sistema entre no endereço:
  
    localhost:8000
