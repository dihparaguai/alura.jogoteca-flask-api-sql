# 'render_template' > por padrao olha os arquivos dentro do diretorio 'templates'
# 'resquest' > captura os valores dos abritudos 'name' dos arquivos 'html'
# 'redirect' > biblioca com funcoes para redicionamento de paginas
# 'session' > cookies do navegador, que guardar algumas informacoes, como nome do usuario logado
# 'flash' > passar texo e informacoes para 'alert()' no navegador de forma personalizada
# 'url_for' > permite passar a funcao que renderiza a pagina/rota html para o 'redirect()'
# 'send_from_directory' > busca um arquivo/imagem em um diretorio para enviar para a pagina/rota
from flask import render_template, request, redirect, send_from_directory, session, flash, url_for

# 'time' > possui funcoes de data / hora
import time

from jogoteca import db, app
from modules import Usuarios, Jogos
from helpers import Formulario_jogo, FormularioUsuario, deleta_capa_antiga, recupera_capa

# rota da api
@app.route('/')
def index():

    # 'render_template' > funcao do flask para conectar com o 'html'
    # 'titulo' > variavel criada com dupla-chaves no arquivo html '{{ }}'
    # 'lista_jogos' > sera enviado ao 'html' que vai iterar sobre ela utilizando 'foreach'
    # 'Jogos.query.order_by()' realiza leitura no banco de dados
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista_jogos = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='jogos', jogos=lista_jogos)


# rota de pagina html, com formulario de cadastro
@app.route('/novo')
def novo():

    # se nao existir sessao ou se a chave 'usuario_logado' for igual a none
    # garante que se o usuario nao estiver loga, entao noa acessarava esta pagina
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=novo')
    form = Formulario_jogo()
    return render_template('novo.html', titulo='novo jogo', form=form)


# rota intermediaria, que recebe os valores do formulario sem passar pelo url do navegador
@app.route('/criar', methods=['POST',])
def criar():
    form = Formulario_jogo(request.form)

    if form.validate_on_submit():
        return redirect(url_for('novo'))
    
    # atributos do formulario de cadastro
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    # verifica se o jogo que sera cadastrado ja existe no banco de dados
    if Jogos.query.filter_by(nome=nome).first():
        return redirect(url_for('index'))

    # instancia um objeto de banco de dados com as informacoes do cadastro do jogo
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)

    # adiciona o objeto do jogo ao banco de dados
    db.session.add(novo_jogo)
    db.session.commit()

    # busca o arquivo atraves do 'resquest.files[]' e do 'name', para salvar na pasta 'uploads/'
    # o nome do arquivo a ser salvo contem o numero do id e nome do novo jogo adicionado
    arquivo = request.files['arquivo']

    # usa o 'app.config[]' do Flask para buscar no dicionario formado pelo nome das variaveis que estao no arquivo 'config.py', e assim utilizar os dados atribuitos em 'UPLOAD_PATH'
    upload_path = app.config['UPLOADS_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    # retorno para a rota '/' (index)
    # url_for utiliza a funcao da rota ao inves pagina da rota
    return redirect(url_for('index'))


# rota de pagina html, com formulario de editar um item cadastrado
# ao clicar em algum jogo, id recebido via parametro do 'url_for'
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=editar')

    # renderiza a pagina 'editar.html' com os dados do jogo que foi selecionado na pagina de lista
    jogo = Jogos.query.filter_by(id=id).first()
    
    form = Formulario_jogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_capa(id)
    return render_template('editar.html', titulo='editar jogo', id=id, capa_jogo=capa_jogo, form=form)


# rota intermediaria, que atualiza um item selecionado na lista de jogos
@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = Formulario_jogo(request.form)
    
    if form.validate_on_submit():

        # para atualizar o jogo, as novas informações sobrescrevem os dados que estavam no banco de dados
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.console.data
        jogo.console = form.console

        # ao adicionar o jogo com o mesmo id, ele sobrescreve o que estava gravado no banco de dado
        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOADS_PATH']
        
        # retorna o momento atual
        timestamp = time.time()
        
        # deleta o antigo antigo, para nao ficar arquivos orfãos armazenados
        deleta_capa_antiga(jogo.id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

        # retorno para a rota '/' (index)
        # url_for utiliza a funcao da rota ao inves pagina da rota
    return redirect(url_for('index'))


# rota intermediaria, que deleta um item selecionado na lista de jogos
@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')

    # deleta a linha com a chave do jogo selecionado, pra isso recebe o id do jogo atraves do 'url_for'
    Jogos.query.filter_by(id=id).delete()
    
    # deleta o arquivo vinculado ao registro que também foi deletado
    deleta_capa_antiga(id)
    db.session.commit()

    flash('jogo deletado com sucesso')
    return redirect(url_for('index'))


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

    # caso o ususario exista...
    if usuario:

        # verifica se este usuario fitrado possui a mesma senha que foi digitada
        if form.senha.data == usuario.senha:

            # 'session' permite armazenar dados de cookies, mas para isso, precisa de '.secretkey' para criptografar os cookies
            session['usuario_logado'] = usuario.nickname

            # 'flash' permite mostrar um 'alert()' personalizado no navegador, usando as inforacoes que estavam nos cookies, devido ao 'session'
            flash(usuario.nickname + ' logado com sucesso')

            # apos as conferencias, a pagina rediciona para a proxima pagina que estava configurada para a variavel 'proxima', conhecinha por 'query string'
            # caso nao seja passado nenhum parametro de URL, entao seja redirecionado para a pagina principal
            proxima_pagina = "" if request.form['proxima'] == "None" else request.form['proxima']
            print(proxima_pagina)
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


# a rota 'imagem' recebe o nome da imagem (capa_padrao) do html e usando o'send_from_directory', busca a imagem no diretorio 'uploads' e envia ela para o html
@app.route('/imagem/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
