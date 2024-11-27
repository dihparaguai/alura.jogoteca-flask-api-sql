# classe 'Jogo' e 'Usuario'
from modules.jogo import Jogo
from modules.usuario import Usuario

# permite utilizar o 'ORM' que realiza a integracao e conexao entre o 'Flask' e o banco de dados 'MySQL'
# o 'ORM' utulizado sera o 'SQLAlchemy'
from flask_sqlalchemy import SQLAlchemy


# 'render_template' > por padrao olha os arquivos dentro do diretorio 'templates'
# 'resquest' > captura os valores dos abritudos 'name' dos arquivos 'html'
# 'redirect' > biblioca com funcoes para redicionamento de paginas
# 'session' > cookies do navegador, que guardar algumas informacoes, como nome do usuario logado
# 'flash' > passar texo e informacoes para 'alert()' no navegador de forma personalizada
# 'url_for' > permite passar a funcao que renderiza a pagina/rota html para o 'redirect()'
from flask import Flask, render_template, request, redirect, session, flash, url_for


# 'Flask()' > classe que possui os comandos de http e api
# '__name__' > referencia o nome do proprio arquivo
app = Flask(__name__)

# criptografa os cookies, para ser usando em conunto com 'session[]'
app.secret_key = 'chave_secreta'

# realiza a configuracao da porta e conexao entre a classe  'Flask' que foi atribuido a variavel 'app' e o banco de dados 'MySQL' atraves do 'ORM' 'SQLAlchemy'
# = \ (contra-barra) informa ao python que sera feita uma quebra de linha intencional
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='admin',
        servidor='localhost',
        database='jogoteca'
)

# inicializa o 'ORM' entre o banco de dados, atraves da classe 'SQLAlchemy', e a classe 'Flask', passando a variavel 'app' (classe 'Flask') como parametro para o 'ORM' na classe de 'SQLAlchemy'
db = SQLAlchemy(app)

# instancia estaticamente cada jogo com suas caracteristicas
jogo1 = Jogo('god of war', 'aventura', 'play 2')
jogo2 = Jogo('naruto', 'luta', 'ps3')
jogo3 = Jogo('mortal kombat', 'luta', 'ps2')
jogo4 = Jogo('league of legends', 'luta', 'pc')

# adiciona na lista de jogos, cada objeto de jogo
lista_jogos = [jogo1, jogo2, jogo3, jogo4]


# instancia estatica de cad usuario com suas caracteristicas
usuario1 = Usuario('bruno', 'bd', 'alohomora')
usuario2 = Usuario('camila', 'mila', 'paozinho')
usuario3 = Usuario('guilherme', 'cake', 'python eh vida')
usuario4 = Usuario('diego paraguai', 'paraguai', '1235')

# adiciona em um 'dicionario' chave='nickname' e valor='usuario'(objeto)
lista_usuarios = {
    usuario1.nickname: usuario1,
    usuario2.nickname: usuario2,
    usuario3.nickname: usuario3,
    usuario4.nickname: usuario4
}


# rota da api
@app.route('/')
def index():

    # 'render_template' > funcao do flask para conectar com o 'html'
    # 'titulo' > variavel criada com dupla-chaves no arquivo html '{{ }}'
    # 'lista_jogos' > sera enviado ao 'html' que vai iterar sobre ela utilizando 'foreach'
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=')
    return render_template('lista.html', titulo='jogos', jogos=lista_jogos)


# rota de pagina html, com formulario de cadastro
@app.route('/novo')
def novo():

    # se nao existir sessao ou se a chave 'usuario_logado' for igual a none
    # garante que se o usuario nao estiver loga, entao noa acessarava esta pagina
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=novo')
    return render_template('novo.html', titulo='novo jogo')


# rota de intermediaria, que recebe os valores do formulario sem passar pelo url do navegador
@app.route('/criar', methods=['POST',])
def criar():

    # atributos do formulario de cadastro
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    # objeto jogo que vai receber os atributos
    jogo = Jogo(nome, categoria, console)

    # lista de objetos jogos
    lista_jogos.append(jogo)

    # retorno para a rota '/' (index)
    # url_for utiliza a funcao da rota ao inves pagina da rota
    return redirect(url_for('index'))


# rota de pagina html, com formulario de login
@app.route('/login')
def login():

    # recupera a informacao que foi passada para a 'query string', ou seja, o valor que estiver na variavel 'proxima' na url
    proxima = request.args.get('proxima')

    # renderiza a pagina login, ja passando a 'query string' que foi recebida pela variavel
    return render_template('login.html', proxima=proxima)


# rota de intermediaria, que valida as informacoes de login antes de passar para a pagina 'index'
@app.route('/autenticar', methods=['POST',])
def autenticar():

    # verifica que o usuario digitado esta em uma chave do dicionario 'lista_usuarios'
    if request.form['usuario'] in lista_usuarios:

        # caso 'usuario' seja encontrado no dicionario, entao armazena o seu nickname e utiliza-o para conferir se a senha deste 'usuario' confere com o valor cadastrado no objeto dele
        usuario = lista_usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:

            # 'session' permite armazenar dados de cookies, mas para isso, precisa de '.secretkey' para criptografar os cookies
            session['usuario_logado'] = usuario.nickname

            # 'flash' permite mostrar um 'alert()' personalizado no navegador, usando as inforacoes que estavam nos cookies, devido ao 'session'
            flash(usuario.nickname + ' logado com sucesso')

            # apos as conferencias, a pagina rediciona para a proxima pagina que estava configurada para a variavel 'proxima', conhecinha por 'query string'
            proxima_pagina = request.form['proxima']
            return redirect('/' + proxima_pagina)

        else:
            flash('usuario ou senha invalido')

            # url_for utiliza a funcao da rota ao inves pagina da rota
            return redirect(url_for('login'))


# rota intermediaria, que remove as informacoes de usuario dos cookies para fazer 'logout'
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('logout efetuado com sucesso')

    # url_for utiliza a funcao da rota ao inves pagina da rota
    return redirect(url_for('login'))


# coloca o servidor flask para rodar
# 'debug=True' reinicializa o servidor automaticamente
app.run(debug=True)
