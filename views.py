from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import db, app
from modules import Usuarios, Jogos

# rota da api
@app.route('/')
def index():
    
    # 'render_template' > funcao do flask para conectar com o 'html'
    # 'titulo' > variavel criada com dupla-chaves no arquivo html '{{ }}'
    # 'lista_jogos' > sera enviado ao 'html' que vai iterar sobre ela utilizando 'foreach'
    # 'Jogos.query.order_by()' realiza leitura no banco de dados
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=')
    lista_jogos = Jogos.query.order_by(Jogos.id)
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

    # verifica se o jogo que sera cadastrado ja existe no banco de dados
    if Jogos.query.filter_by(nome=nome).first():
        return redirect(url_for('index'))
    
    # instancia um objeto de banco de dados com as informacoes do cadastro do jogo
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    
    # adiciona o objeto do jogo ao banco de dados
    db.session.add(novo_jogo)
    db.session.commit()

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
    
    # busca e filtra no banco de dados nome do usuario digitado no formulario html
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    
    # caso o ususario exista...
    if usuario:
        
        # verifica se este usuario fitrado possui a mesma senha que foi digitada 
        if request.form['senha'] == usuario.senha:
                
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