# classe jogo
from modules.jogo import Jogo


# 'render_template' por padrao olha os arquivos dentro do diretorio 'templates'
# para obter os valores do formulario, foi importado 'resquest'
# 'redirect' corresponde a uma biblioca com funcoes para redicionamento de paginas
from flask import Flask, render_template, request, redirect



# '__name__' referencia o nome do proprio arquivo
app = Flask(__name__)



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
    # 'render_template' funcao do flask para conectar com o 'html'
    # 'titulo' corresponde a variavel criada com dupla-chaves no arquivo html '{{ }}'
    # 'lista_jogos' sera enviado ao 'html' que vai iterar sobre ela utilizando 'foreach'
    return render_template('lista.html', titulo='jogos', jogos=lista_jogos)



# rota de outra pagina html, com formulario de cadastro
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


# coloca o servidor flask para rodar
# 'debug=True' reinicializa o servidor automaticamente
app.run(debug=True)
