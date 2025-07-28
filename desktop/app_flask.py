from flask import Flask, jsonify
import os
import shutil
from datetime import datetime

app = Flask(__name__)

CAMINHO_COMANDO = 'comando.json'
DIRETORIO_HISTORICO = 'historico_de_comandos'
os.makedirs(DIRETORIO_HISTORICO, exist_ok=True)

@app.route('/salvar_comando', methods=['GET'])
def salvar_comando():
    if not os.path.isfile(CAMINHO_COMANDO):
        return jsonify({"status": "erro", "mensagem": "Arquivo comando.json não encontrado"}), 404

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nome_arquivo = f"comando_{timestamp}.json"
    caminho_destino = os.path.join(DIRETORIO_HISTORICO, nome_arquivo)

    try:
        # Copia o arquivo para o histórico
        shutil.copy2(CAMINHO_COMANDO, caminho_destino)
        
        # Limpa o comando.json, escrevendo uma lista vazia
        with open(CAMINHO_COMANDO, 'w') as f:
            f.write('[]')

        return jsonify({"status": "sucesso", "arquivo_salvo": caminho_destino})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


def start_flask():
    app.run(port=5000, debug=False, use_reloader=False)