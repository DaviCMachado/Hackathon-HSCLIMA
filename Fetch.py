import os.path
import json
from ConexaoBanco import Conexao

def fetch_data():
    if os.path.isfile('keys.json'):
        with open('keys.json', 'r') as json_file:
            config = json.load(json_file)

        conexao = Conexao(config['host'], config['user'], config['password'], config['database'])

        # Obter dados de todas as tabelas
        produtos = conexao.select('*', config['database'], 'Produto')
        status = conexao.select('*', config['database'], 'Status')
        regioes = conexao.select('*', config['database'], 'Regiao')
        regiao_produto = conexao.select('*', config['database'], 'RegiaoProduto')

        # Estruturar os dados em um formato relacionável
        data = {
            "produtos": [
                {"cod": row[0], "nome": row[1], "tipoQtd": row[2]}
                for row in produtos
            ],
            "status": [
                {"cod": row[0], "descricao": row[1]}
                for row in status
            ],
            "regioes": [
                {"cod": row[0], "latitude": row[1], "longitude": row[2], "raio": row[3], "codStatus": row[4]}
                for row in regioes
            ],
            "regiao_produto": [
                {"codProduto": row[0], "codRegiao": row[1], "quantidade": row[2]}
                for row in regiao_produto
            ]
        }

        # Criar ou atualizar o arquivo data.json
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print("Arquivo 'data.json' criado/atualizado.")

    else:
        print("Arquivo 'keys.json' não encontrado.\n\nCrie o arquivo 'keys.json' com as informações de conexão com o banco de dados")

if __name__ == '__main__':
    fetch_data()
