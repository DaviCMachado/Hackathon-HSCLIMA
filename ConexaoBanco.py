import mysql.connector

class Conexao:
    def __init__(self, host, user, password, database):
        self.user = user
        self.host = host
        self.database = database
        self.conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def createDatabase(self):
        sql = "CREATE DATABASE %s " % self.database
        cursor = self.conexao.cursor()
        cursor.execute(sql)

    def createTable(self, nameTable: str, fields: dict, other_data: list):
        cursor = self.conexao.cursor()
        command = "CREATE TABLE %s (%s)" % (
            nameTable,
            ','.join([k + ' ' + v for k, v in fields.items()] + (
                other_data if other_data is not None else []))
        )
        cursor.execute(command)

    def select(self, column: str, database: str,table: str):
        cursor = self.conexao.cursor()
        command = 'SELECT %s FROM %s.%s;' % (column, database, table)
        cursor.execute(command)
        rows = cursor.fetchall()
        return rows

##fora da class
def createDatabase():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
        )
        cursor = conexao.cursor()
        cursor.execute('CREATE DATABASE hsclima')
        conexao.close()
    except Exception as e:
        print(e)

def inicializaTabelas():
    conexao = Conexao('localhost', 'root', 'root', 'hsclima')
    try:
        conexao.createTable(
            'Status',
            {
                'cod':'INT',
                'descricao':'TEXT'
            },
            [
                'PRIMARY KEY (cod)'
            ]
        )
    except Exception as e:
        print(e)

    try:
        conexao.createTable(
            'Produto',
            {
                'cod':'INT',
                'nome':'TEXT NOT NULL',
                'tipoQtd':'TEXT NOT NULL'
            },
            [
                'PRIMARY KEY (cod)'
            ]
        )
    except Exception as e:
        print(e)


    try:
        conexao.createTable(
            'Regiao',
            {
                'cod':'INT',
                'latitude':'FLOAT', ## CONFERIR SE É A MELHOR FORMA DE SALVAR COORDS
                'longitude':'FLOAT',
                'raio':'FLOAT',
                'codStatus':'INT'
            },
            [
                'PRIMARY KEY (cod)',
                'FOREIGN KEY (codStatus) REFERENCES Status(cod)'
            ]
        )
    except Exception as e:
        print(e)

    try:
        conexao.createTable(
            'RegiaoProduto',
            {
                'codRegiao':'INT',
                'codProduto':'INT',
                'quantidade':'FLOAT'
            },
            [
                'FOREIGN KEY (codRegiao) REFERENCES Regiao(cod)',
                'FOREIGN KEY (codProduto) REFERENCES Produto(cod)'
            ]
        )
    except Exception as e:
        print(e)



createDatabase()
inicializaTabelas()