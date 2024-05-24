import os.path
import json
from ConexaoBanco import Conexao

def fetch_data():
    if os.path.isfile('keys.json'):
        with open('keys.json', 'r') as json_file:
            config = json.load(json_file)

        conexao = Conexao(config['host'], config['user'], config['password'], config['database'])

        rows = conexao.select('*', config['database'], 'RegiaoProduto')  # Ajustar a consulta
        data = [{"codRegiao": row[0], "codProduto": row[1], "quantidade": row[2]} for row in rows]

        if not os.path.isfile('data.json'):
            with open('data.json', 'w') as json_file:
                json.dump(data, json_file)
            print("Arquivo 'data.json' criado.")
        else:         
            with open('data.json', 'w') as json_file:
                json.dump(data, json_file)
            print("Arquivo 'data.json' atualizado.")

    else:
        print("Arquivo 'keys.json' não encontrado.\n\nCrie o arquivo 'keys.json' com as informações de conexão com o banco de dados")

if __name__ == '__main__':
    fetch_data()
