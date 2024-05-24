import os.path
import json
from ConexaoBanco import Conexao

def insere_novos_dados(codProduto, codRegiao):

    if os.path.isfile('keys.json'):
        with open('keys.json', 'r') as json_file:
            config = json.load(json_file)

        conexao = Conexao(config['host'], config['user'], config['password'], config['database'])

        conexao.dropAllTables()

        # Insira aqui o código para inserir os novos dados utilizando os métodos da classe Conexao
        conexao.insertStatus(codRegiao, 'Novo status')
        conexao.insertProduto(codProduto, 'Novo produto', 'Tipo novo')
        conexao.insertRegiao(codProduto, 0.0, 0.0, 10.0, 1)
        conexao.insertRegiaoProduto(codProduto, codRegiao, 10.0)

    else:
        print("Arquivo 'keys.json' não encontrado.\n\nCrie o arquivo 'keys.json' com as informações de conexão com o banco de dados")




if __name__ == '__main__':
    codProduto = 911
    codRegiao = 911
    insere_novos_dados(codProduto, codRegiao)
