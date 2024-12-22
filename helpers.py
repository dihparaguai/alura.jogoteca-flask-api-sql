import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class Formulario_jogo(FlaskForm):
    nome = StringField('nome do jogo', [validators.DataRequired(), validators.Length(max=50, min=1)])
    categoria = StringField('categoria', [validators.DataRequired(), validators.Length(max=40, min=1)])
    console = StringField('console', [validators.DataRequired(), validators.Length(max=20, min=1)])
    salvar = SubmitField('salvar')
    

# busca na pasta de arquivos o nome o arquivo especifico
def recupera_capa(id):
    
    # 'os.listdir()' percorre o nome dos arquivos no caminho espeficado
    for nome_jogo in os.listdir(app.config['UPLOADS_PATH']):
        
        # para cada item na lista, comparar com o id recebido
        if f'capa{id}' in nome_jogo:
            return nome_jogo
    
    return 'capa_padrao.jpg'


# deleta o arquivo antigo após a atualizacao do novo arquivo
def deleta_capa_antiga(id):
    capa = recupera_capa(id)
    
    # nao pode deletar a 'capa_padrao.jpg'
    if capa != 'capa_padrao.jpg':
        
        # remove a capa do jogo que que possui o mesmo nome do que foi recuperado em 'recupera_capa()' dp caminho da pasta 'uploads/'
        os.remove(os.path.join(app.config['UPLOADS_PATH'], capa))
