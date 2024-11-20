from jogo import Jogo

# 'render_template' por padrao olha os arquivos dentro do diretorio 'templates'
from flask import Flask, render_template

# '__name__' referencia o nome do proprio arquivo
app = Flask(__name__)

# rota da api
@app.route('/inicio')
def ola():
    # instancia cada jogo com suas caracteristicas
    jogo1 = Jogo('god of war', 'aventura', 'play 2')
    jogo2 = Jogo('naruto', 'luta', 'ps3')
    jogo3 = Jogo('mortal kombat', 'luta', 'pc')
    
    # adiciona na lista de jogos, cada objeto de jogo
    lista_jogos = [jogo1, jogo2, jogo3]

    # 'render_template' funcao do flask para conectar com o 'html'
    # 'titulo' corresponde a variavel criada com dupla-chaves no arquivo html '{{ }}'
    # 'lista_jogos' sera enviado ao 'html' que vai iterar sobre ela utilizando 'foreach'
    return render_template('lista.html', titulo='jogos', jogos=lista_jogos)

# coloca o servidor flask para rodar
app.run()
