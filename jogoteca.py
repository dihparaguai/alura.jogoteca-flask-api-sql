# 'render_template' > por padrao olha os arquivos dentro do diretorio 'templates'
# 'resquest' > captura os valores dos abritudos 'name' dos arquivos 'html'
# 'redirect' > biblioca com funcoes para redicionamento de paginas
# 'session' > cookies do navegador, que guardar algumas informacoes, como nome do usuario logado
# 'flash' > passar texo e informacoes para 'alert()' no navegador de forma personalizada
# 'url_for' > permite passar a funcao que renderiza a pagina/rota html para o 'redirect()'
from flask import Flask

# permite utilizar o 'ORM' que realiza a integracao e conexao entre o 'Flask' e o banco de dados 'MySQL'
# o 'ORM' utulizado sera o 'SQLAlchemy'
from flask_sqlalchemy import SQLAlchemy

# 'Flask()' > classe que possui os comandos de http e api
# '__name__' > referencia o nome do proprio arquivo
app = Flask(__name__)

#
app.config.from_pyfile('config.py')

# inicializa o 'ORM' entre o banco de dados, atraves da classe 'SQLAlchemy', e a classe 'Flask', passando a variavel 'app' (classe 'Flask') como parametro para o 'ORM' na classe de 'SQLAlchemy'
db = SQLAlchemy(app)

#
from views import *

# coloca o servidor flask para rodar
# 'debug=True' reinicializa o servidor automaticamente
if __name__ == '__main__':
    app.run(debug=True)
