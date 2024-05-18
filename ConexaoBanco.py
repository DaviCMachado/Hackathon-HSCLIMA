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

    def createTable(self, name_table: str, fields: dict, other_data: list):
        cursor = self.conexao.cursor()
        command = "CREATE TABLE %s (%s)" % (
            name_table,
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

    def insertStatus(self, cod: int, descricao: str):
        cursor = self.conexao.cursor()
        sql = 'INSERT INTO hsclima.Status(cod, descricao) VALUES (%d, "%s");' % (cod, descricao)
        cursor.execute(sql)
        self.conexao.commit()


    def insertProduto(self, cod: int, nome: str, tipoQtd: str):
        cursor = self.conexao.cursor()
        sql = 'INSERT INTO hsclima.Produto(cod, nome, tipoQtd) VALUES(%d, "%s", "%s")' % (cod, nome, tipoQtd)
        cursor.execute(sql)
        self.conexao.commit()

    def insertRegiao(self, latitude, longitude, raio, codStatus):
        cursor = self.conexao.cursor()
        sql = 'INSERT INTO hsclima.Regiao(latitude, longitude, raio, codStatus) VALUES (%f, %f, %f, %d)' % (
            latitude, longitude, raio, codStatus
        )
        cursor.execute(sql)
        self.conexao.commit()

    def insertRegiaoProduto(self, codProduto, codRegiao, quantidade):
        cursor = self.conexao.cursor()
        sql = 'INSERT INTO hsclima.RegiaoProduto(codProduto, codRegiao, quantidade) VALUES (%d, %d, %f)' % (codProduto, codRegiao, quantidade)
        cursor.execute(sql)
        self.conexao.commit()


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
                'PRIMARY KEY AUTO_INCREMENT (cod)',
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


def defineStatus():
    try:
        conexao = Conexao('localhost', 'root', 'root', 'hsclima')
        conexao.insertStatus(1, 'Necessita limpeza')
        conexao.insertStatus(2, 'Necessita reconstrução')
        conexao.insertStatus(3, 'Necessita limpeza e reconstrução')
    except Exception as e:
        print(e)

createDatabase()
inicializaTabelas()
defineStatus()