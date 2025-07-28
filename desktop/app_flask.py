from flask import Flask, jsonify
import os
import shutil
from datetime import datetime

app = Flask(__name__)

from flask import Flask, jsonify
import os
import shutil
from datetime import datetime
import json

app = Flask(__name__)

CAMINHO_COMANDO = 'comando.json'
DIRETORIO_HISTORICO = 'historico_de_comandos'
os.makedirs(DIRETORIO_HISTORICO, exist_ok=True)

DATA_CHAVE = "_data_registro_"  # Nome especial para guardar data/hora

@app.route('/gravar_data_comando', methods=['GET'])
def registrar_data_comando():
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Lê o conteúdo atual
    comandos = []
    if os.path.exists(CAMINHO_COMANDO):
        with open(CAMINHO_COMANDO, 'r') as f:
            try:
                comandos = json.load(f)
            except Exception:
                comandos = []

    # Adiciona a marca de data
    comandos.append({DATA_CHAVE: data_hora})

    # Salva de volta
    with open(CAMINHO_COMANDO, 'w') as f:
        json.dump(comandos, f, indent=2)

    return jsonify({"status": "gravacao iniciada com sucesso", "data_hora": data_hora})






@app.route('/salvar_comando', methods=['GET'])
def salvar_comando():
    if not os.path.isfile(CAMINHO_COMANDO):
        return jsonify({"status": "erro", "mensagem": "Arquivo comando.json não encontrado"}), 404

    try:
        with open(CAMINHO_COMANDO, 'r') as f:
            comandos = json.load(f)

        # Encontra a última marca de tempo registrada
        data_inicio = None
        for i in reversed(range(len(comandos))):
            if isinstance(comandos[i], dict) and DATA_CHAVE in comandos[i]:
                data_inicio = comandos[i][DATA_CHAVE]
                comandos = comandos[i+1:]  # mantém apenas comandos depois da marca
                break

        if data_inicio is None:
            return jsonify({"status": "erro", "mensagem": "Nenhuma data registrada encontrada"}), 400

        # Salva comandos filtrados com nome baseado na data
        timestamp = datetime.strptime(data_inicio, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d_%H%M%S')
        nome_arquivo = f"comando_{timestamp}.json"
        caminho_destino = os.path.join(DIRETORIO_HISTORICO, nome_arquivo)

        with open(caminho_destino, 'w') as f:
            json.dump(comandos, f, indent=2)

        # Limpa comando.json
        with open(CAMINHO_COMANDO, 'w') as f:
            json.dump([], f)

        return jsonify({"status": "gravacao salva com sucesso", "arquivo_salvo": caminho_destino})

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500



    




@app.route('/listar_comandos', methods=['GET'])
def listar_comandos():
    try:
        arquivos = os.listdir(DIRETORIO_HISTORICO)
        jsons = [f for f in arquivos if f.endswith('.json')]
        return jsonify({"status": "sucesso", "arquivos": jsons})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    




@app.route('/obter_comando/<nome_arquivo>', methods=['GET'])
def obter_comando(nome_arquivo):
    caminho = os.path.join(DIRETORIO_HISTORICO, nome_arquivo)
    if not os.path.isfile(caminho):
        return jsonify({"status": "erro", "mensagem": "Arquivo não encontrado"}), 404

    try:
        with open(caminho, 'r') as f:
            conteudo = f.read()
        return jsonify({"status": "sucesso", "conteudo": conteudo})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


def start_flask():
    app.run(port=5000, debug=False, use_reloader=False)