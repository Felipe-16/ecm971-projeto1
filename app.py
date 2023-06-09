from flask import Flask, jsonify, request
from tabulate import tabulate

app = Flask(__name__)

musicas = [
    {
        'id' : 1,
        'nome' : 'demons', 
        'avaliacao' : 5
    },
]

# Função para verificar se o nome da música já existe
def verificar_nome_musica(nome):
    for musica in musicas:
        if musica['nome'] == nome:
            return musica
    return False

# # Rota para listar todas as músicas
@app.route('/musicas', methods=['GET'])
def listar_musicas():
    ordem_musicas = sorted(musicas, key=lambda x: x['avaliacao'], reverse=True)
    tabela = []
    for musica in ordem_musicas:
        tabela.append([musica['id'], musica['nome'], musica['avaliacao']])

    cabecalho = ['ID', 'Nome da Música', 'Avaliação']
    tabela = tabulate(tabela, headers=cabecalho, tablefmt='grid')

    return tabela


# Rota para cadastrar uma música
@app.route('/musicasPost', methods=['POST'])
def cadastrar_musica():
    nome = request.json['nome'].lower()
    
    # Verifica se o nome da música já existe
    if verificar_nome_musica(nome):
        return jsonify({'message': 'O nome da música já existe. Escolha outro nome.'}), 400
    
    # Criação do objeto da música
    musica = {
        'id': len(musicas) + 1,  # Identificador automático
        'nome': nome,
        'avaliacao': 0  # Avaliação inicial
    }
    
    # Adiciona a música à lista de músicas
    musicas.append(musica)
    
    return jsonify(musica), 201

#Rota para avaliar uma musica
@app.route('/musicas/avaliacao', methods=['POST'])
def avaliar_musica():
    nome = request.json['nome'].lower()
    avaliacao = int(round(request.json['avaliacao'],0))

    musica = verificar_nome_musica(nome)
    if not musica:
        return jsonify({'error': 'Música não encontrada.'}), 404

    if avaliacao < 1 or avaliacao > 5:
        return jsonify({'error': 'Nota inválida. Insira valores entre 1 e 5.'}), 400

    musica['avaliacao'] = avaliacao
    return jsonify(musica)




app.run(port=5000,host='localhost', debug=True)

