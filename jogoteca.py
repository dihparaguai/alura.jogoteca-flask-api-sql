# classe jogo
from modules.jogo import Jogo


# 'render_template' > por padrao olha os arquivos dentro do diretorio 'templates'
# 'resquest' > captura os valores dos abritudos 'name' dos arquivos 'html'
# 'redirect' > biblioca com funcoes para redicionamento de paginas
# 'session' > cookies do navegador, que guardar algumas informacoes, como nome do usuario logado
# 'flash' > passar texo e informacoes para 'alert()' no navegador de forma personalizada
from flask import Flask, render_template, request, redirect, session, flash



# 'Flask()' > classe que possui os comandos de http e api
# '__name__' > referencia o nome do proprio arquivo
app = Flask(__name__)

# criptografa os cookies, para ser usando em conunto com 'session[]'
app.secret_key = 'chave_secreta'



# instancia estaticamente cada jogo com suas caracteristicas
jogo1 = Jogo('god of war', 'aventura', 'play 2')
jogo2 = Jogo('naruto', 'luta', 'ps3')
jogo3 = Jogo('mortal kombat', 'luta', 'ps2')
jogo4 = Jogo('league of legends', 'luta', 'pc')

# adiciona na lista de jogos, cada objeto de jogo
lista_jogos = [jogo1, jogo2, jogo3, jogo4]



# rota da api
@app.route('/')
def index():
    # 'render_template' > funcao do flask para conectar com o 'html'
    # 'titulo' > variavel criada com dupla-chaves no arquivo html '{{ }}'
    # 'lista_jogos' > sera enviado ao 'html' que vai iterar sobre ela utilizando 'foreach'
    return render_template('lista.html', titulo='jogos', jogos=lista_jogos)



# rota de pagina html, com formulario de cadastro
@app.route('/novo')
def novo_jogo():
    return render_template('novo.html', titulo='novo jogo')



# rota de intermediaria, que recebe os valores do formulario sem passar pelo url do navegador
@app.route('/criar', methods=['POST',])
def criar_jogo():

    # atributos do formulario de cadastro
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    # objeto jogo que vai receber os atributos
    jogo = Jogo(nome, categoria, console)

    # lista de objetos jogos
    lista_jogos.append(jogo)

    # retorno para a rota '/' (index)
    return redirect('/')



# rota de pagina html, com formulario de login
@app.route('/login')
def login():
    return render_template('/login.html')



# rota de intermediaria, que valida as informacoes de login antes de passar para a pagina 'index'
@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'alohomora' == request.form['senha']:
        
        # 'session' permite armazenar dados de cookies, mas para isso, precisa de '.secretkey' para criptografar os cookies
        session['usuario_logado'] = request.form['usuario']
        
        # 'flash' permite mostrar um 'alert()' personalizado no navegador, usando as inforacoes que estavam nos cookies, devido ao 'session'
        flash(session['usuario_logado'] + ' logado com sucesso')
        return redirect('/')

    else:
        flash('usuario ou senha invalido')
        return redirect('/login')


# rota intermediaria, que remove as informacoes de usuario dos cookies para fazer 'logout'
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('logout efetuado com sucesso')
    return redirect('/login')



# coloca o servidor flask para rodar
# 'debug=True' reinicializa o servidor automaticamente
app.run(debug=True)
