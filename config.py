import os

# criptografa os cookies, para ser usando em conjunto com 'session[]'
SECRET_KEY = 'chave_secreta'

# realiza a configuracao da porta e conexao entre a classe  'Flask' que foi atribuido a variavel 'app' e o banco de dados 'MySQL' atraves do 'ORM' 'SQLAlchemy'
# = \ (contra-barra) informa ao python que sera feita uma quebra de linha intencional
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        # caso algum dia, mude o banco de dados a ser usado, basta alterar a informaçao do 'SGBD'
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='admin',
        servidor='localhost',
        database='jogoteca'
    )

# '__file__' > retorna o caminho absoluto ou relativo até o arquivo atual, por isso é usado em conjunto com 'os.path.abspath()' para garantir o caminho completo absoluto
# 'os.path.abspath()' > retorna o caminho absoluto completo até o arquivo passado como parametro = exemplo: "../arquivo.txt" vira "C:\Users\diego\arquivo.txt"
# 'os.path.dirname()' > retorna o caminho absoluto completo até o diretorio do arquivo passao como parametro = exemplo: "C:\Users\diego\arquivo.txt" vira "C:\Users\diego"
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__))+'/uploads'