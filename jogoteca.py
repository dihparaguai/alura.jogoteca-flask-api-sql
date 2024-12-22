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

# a partir do 'flask_wtf', deve-se utilizar o CSRF para garantir segurança em formularios web
from flask_wtf.csrf import CSRFProtect

# 'Flask()' > classe que possui os comandos de http e api
# '__name__' > referencia o nome do proprio arquivo
app = Flask(__name__)

# '.config.from_pyfile()' adiciona todas as variaveis do arquivo 'config.py' num dicionario, e o Flask acessa automaticamente os dados atribuido a essas variaveis atraves dos nomes das chaves padronizadas = exemplo para configuracoes do banco de dados com sqlalchemy, o nome da variavel deve ser 'SQLALCHEMY_DATABASE_URI'
app.config.from_pyfile('config.py')

# inicializa o 'ORM' entre o banco de dados, atraves da classe 'SQLAlchemy', e a classe 'Flask', passando a variavel 'app' (classe 'Flask') como parametro para o 'ORM' na classe de 'SQLAlchemy'
db = SQLAlchemy(app)

# funciona como um token, que gera numeros aleatorios, garantindo a segurança em formularios 'html'
crf = CSRFProtect(app)

# importa tudo que esta no arquivo 'views.py'
from views import *

# coloca o servidor flask para rodar
# 'debug=True' reinicializa o servidor automaticamente
if __name__ == '__main__':
    app.run(debug=True)
