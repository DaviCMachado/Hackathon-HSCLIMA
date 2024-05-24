import mysql.connector

class Conexao:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.createDatabase()

    def createDatabase(self):
        try:
            conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
            )
            cursor = conexao.cursor()
            cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(self.database))
            conexao.close()
        except Exception as e:
            print(e)

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
        try:
            sql = 'INSERT INTO hsclima.Status(cod, descricao) VALUES (%s, %s);'
            cursor.execute(sql, (cod, descricao))
            self.conexao.commit()
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                print(f"Registro com chave primária {cod} já existe na tabela 'Status'.")
            else:
                print(e)


    def insertProduto(self, cod: int, nome: str, tipoQtd: str):
        cursor = self.conexao.cursor()
        sql = 'INSERT INTO hsclima.Produto(cod, nome, tipoQtd) VALUES(%d, "%s", "%s")' % (cod, nome, tipoQtd)
        cursor.execute(sql)
        self.conexao.commit()
    
    def insertRegiao(self, latitude, longitude, raio, codStatus, cod):
        cursor = self.conexao.cursor()
        sql = 'INSERT INTO hsclima.Regiao(latitude, longitude, raio, codStatus) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, (cod, latitude, longitude, raio, codStatus))
        self.conexao.commit()


    def insertRegiaoProduto(self, codProduto, codRegiao, quantidade):
        cursor = self.conexao.cursor()
        sql = 'INSERT INTO hsclima.RegiaoProduto(codProduto, codRegiao, quantidade) VALUES (%d, %d, %f)' % (codProduto, codRegiao, quantidade)
        cursor.execute(sql)
        self.conexao.commit()

    def inicializaTabelas(self):
        try:
            self.createTable(
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
            self.createTable(
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
            self.createTable(
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
            self.createTable(
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

    def defineStatus(self):
        try:
            self.insertStatus(1, 'Necessita limpeza')
            self.insertStatus(2, 'Necessita reconstrução')
            self.insertStatus(3, 'Necessita limpeza e reconstrução')
        except Exception as e:
            print(e)

    def dropAllTables(self):    # usado para testes
        tables = ['Status', 'Produto', 'Regiao', 'RegiaoProduto']
        cursor = self.conexao.cursor()
        try:
            for table in tables:
                cursor.execute(f'DROP TABLE IF EXISTS {table};')  
            self.conexao.commit()
            print("Todas as tabelas foram excluídas com sucesso.")
        except Exception as e:
            print(f"Erro ao excluir tabelas: {e}")

