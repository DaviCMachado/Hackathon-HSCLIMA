import os.path
import json
from ConexaoBanco import Conexao

def insere_novos_dados(codProduto, codRegiao):
    if os.path.isfile('keys.json'):
        with open('keys.json', 'r') as json_file:
            config = json.load(json_file)

        conexao = Conexao(config['host'], config['user'], config['password'], config['database'])

        conexao.dropAllTables()
        conexao.inicializaTabelas()

        # Insira aqui o código para inserir os novos dados utilizando os métodos da classe Conexao
        conexao.insertStatus(codRegiao, 'Novo status')
        conexao.insertProduto(codProduto, 'Novo produto', 'Tipo novo')
        conexao.insertRegiao(codRegiao, 0.0, 0.0, 10.0, 1)
        conexao.insertRegiaoProduto(codProduto, codRegiao, 10.0)

    else:
        print("Arquivo 'keys.json' não encontrado.\n\nCrie o arquivo 'keys.json' com as informações de conexão com o banco de dados")

# Funções CRUD

def criar_status(conexao, cod, descricao):
    conexao.insertStatus(cod, descricao)

def ler_status(conexao, cod):
    return conexao.getStatusByCod(cod)

def atualizar_status(conexao, cod, descricao):
    conexao.updateStatus(cod, descricao)

def deletar_status(conexao, cod):
    conexao.deleteStatus(cod)

def criar_produto(conexao, cod, nome, tipoQtd):
    conexao.insertProduto(cod, nome, tipoQtd)

def ler_produto(conexao, cod):
    return conexao.getProdutoByCod(cod)

def atualizar_produto(conexao, cod, nome, tipoQtd):
    conexao.updateProduto(cod, nome, tipoQtd)

def deletar_produto(conexao, cod):
    conexao.deleteProduto(cod)

def criar_regiao(conexao, cod, latitude, longitude, raio, codStatus):
    conexao.insertRegiao(cod, latitude, longitude, raio, codStatus)

def ler_regiao(conexao, cod):
    return conexao.getRegiaoByCod(cod)

def atualizar_regiao(conexao, cod, latitude, longitude, raio, codStatus):
    conexao.updateRegiao(cod, latitude, longitude, raio, codStatus)

def deletar_regiao(conexao, cod):
    conexao.deleteRegiao(cod)

def criar_regiao_produto(conexao, codProduto, codRegiao, quantidade):
    conexao.insertRegiaoProduto(codProduto, codRegiao, quantidade)

def ler_regiao_produto(conexao, codProduto, codRegiao):
    return conexao.getRegiaoProdutoByCod(codProduto, codRegiao)

def atualizar_regiao_produto(conexao, codProduto, codRegiao, quantidade):
    conexao.updateRegiaoProduto(codProduto, codRegiao, quantidade)

def deletar_regiao_produto(conexao, codProduto, codRegiao):
    conexao.deleteRegiaoProduto(codProduto, codRegiao)

if __name__ == '__main__':

    codProduto = 999
    codRegiao = 999

    if os.path.isfile('keys.json'):
        with open('keys.json', 'r') as json_file:
            config = json.load(json_file)

        conexao = Conexao(config['host'], config['user'], config['password'], config['database'])

        # Exemplos de uso das funções CRUD
        criar_status(conexao, 4, 'Novo status')
        print(ler_status(conexao, 4))
        atualizar_status(conexao, 4, 'Status atualizado')
        print(ler_status(conexao, 4))
        deletar_status(conexao, 4)
        print(ler_status(conexao, 4))

        criar_produto(conexao, codProduto, 'Novo produto', 'Tipo novo')
        print(ler_produto(conexao, codProduto))
        atualizar_produto(conexao, codProduto, 'Produto atualizado', 'Tipo atualizado')
        print(ler_produto(conexao, codProduto))
        deletar_produto(conexao, codProduto)
        print(ler_produto(conexao, codProduto))

        criar_regiao(conexao, codRegiao, 0.0, 0.0, 10.0, 1)
        print(ler_regiao(conexao, codRegiao))
        atualizar_regiao(conexao, codRegiao, 1.0, 1.0, 20.0, 2)
        print(ler_regiao(conexao, codRegiao))
        deletar_regiao(conexao, codRegiao)
        print(ler_regiao(conexao, codRegiao))

        criar_regiao_produto(conexao, codProduto, codRegiao, 10.0)
        print(ler_regiao_produto(conexao, codProduto, codRegiao))
        atualizar_regiao_produto(conexao, codProduto, codRegiao, 20.0)
        print(ler_regiao_produto(conexao, codProduto, codRegiao))
        deletar_regiao_produto(conexao, codProduto, codRegiao)
        print(ler_regiao_produto(conexao, codProduto, codRegiao))

    else:
        print("Arquivo 'keys.json' não encontrado.\n\nCrie o arquivo 'keys.json' com as informações de conexão com o banco de dados")
