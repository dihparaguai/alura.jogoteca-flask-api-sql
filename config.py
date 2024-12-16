# criptografa os cookies, para ser usando em conunto com 'session[]'
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



