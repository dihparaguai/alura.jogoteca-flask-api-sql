# 'render_template' > por padrao olha os arquivos dentro do diretorio 'templates'
# 'resquest' > captura os valores dos abritudos 'name' dos arquivos 'html'
# 'redirect' > biblioca com funcoes para redicionamento de paginas
# 'session' > cookies do navegador, que guardar algumas informacoes, como nome do usuario logado
# 'flash' > passar texo e informacoes para 'alert()' no navegador de forma personalizada
# 'url_for' > permite passar a funcao que renderiza a pagina/rota html para o 'redirect()'
from flask import render_template, request, redirect, session, flash, url_for

# importa a funcao que realiza a comparacao entre senhas hashs
from flask_bcrypt import check_password_hash

from jogoteca import app
from modules import Usuarios
from helpers import FormularioUsuario


# rota de pagina html, com formulario de login
@app.route('/login')
def login():

    # recupera a informacao que foi passada para a 'query string', ou seja, o valor que estiver na variavel 'proxima' na url
    proxima = request.args.get('proxima')

    # instanciacao dos campos de formulario do 'flask_wtf' para validacoes dos inputs
    form = FormularioUsuario()
    
    # renderiza a pagina login, ja passando a 'query string' que foi recebida pela variavel
    return render_template('login.html', proxima=proxima, form=form)


# rota de intermediaria, que valida as informacoes de login antes de passar para a pagina 'index'
@app.route('/autenticar', methods=['POST',])
def autenticar():
    
    # instanciacao dos campos do formulario do 'flask_wtf'
    form = FormularioUsuario()

    # busca e filtra no banco de dados nome do usuario digitado no formulario html
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    
    # caso o ususario exista e a senha hash esteja correta
    if usuario:
        
        # confronta a senha digitada com a senha em hashing no banco de dados
        senha = check_password_hash(usuario.senha, form.senha.data)        
        if senha:

            # 'session' permite armazenar dados de cookies, mas para isso, precisa de '.secretkey' para criptografar os cookies
            session['usuario_logado'] = usuario.nickname

            # 'flash' permite mostrar um 'alert()' personalizado no navegador, usando as inforacoes que estavam nos cookies, devido ao 'session'
            flash(usuario.nickname + ' logado com sucesso')

            # apos as conferencias, a pagina rediciona para a proxima pagina que estava configurada para a variavel 'proxima', conhecinha por 'query string'
            # caso nao seja passado nenhum parametro de URL, entao seja redirecionado para a pagina principal
            proxima_pagina = "" if request.form['proxima'] == "None" else request.form['proxima']
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