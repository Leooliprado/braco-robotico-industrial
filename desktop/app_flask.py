import serial
import serial.tools.list_ports
import time
from datetime import datetime
import os
import json
from flask import Flask, jsonify
from braco_robotico import encontrar_arduino
from flask_cors import CORS 
from plyer import notification


app = Flask(__name__)
CORS(app) 


#=-=-=-=-=-=-=-=-=-=-=-=-=-= caminho para os arquivos na hora que esecuta em .bin ou .exe =-=-=-=-=-=-=-=-=-=-=-=-=-= 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_COMANDO = os.path.join(BASE_DIR, 'comando.json')
DIRETORIO_HISTORICO = os.path.join(BASE_DIR, 'historico_de_comandos')

#=-=-=-=-=-=-=-=-=-=-=-=-=-= caminho para os arquivos na hora que esecuta em .sh ou .bat =-=-=-=-=-=-=-=-=-=-=-=-=-= 

# CAMINHO_COMANDO = 'comando.json'
# DIRETORIO_HISTORICO = 'historico_de_comandos'

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

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

    notification.notify(
        title='Gravação Iniciada',
        message=f'Gravação iniciada com sucesso!',
        timeout=5
    )

    return jsonify({"status": "gravacao iniciada com sucesso", "data_hora": data_hora})






@app.route('/salvar_comando', methods=['GET'])
def salvar_comando():
    if not os.path.isfile(CAMINHO_COMANDO):
        notification.notify(
            title='Erro ao Salvar',
            message=f'Arquivo comando.json não encontrado',
            timeout=5
        )
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

        notification.notify(
            title='Gravação Salva',
            message=f'Gravação salva com sucesso!',
            timeout=5
        )

        return jsonify({"status": "gravacao salva com sucesso", "arquivo_salvo": caminho_destino})

    except Exception as e:
        notification.notify(
            title='Erro ao Salvar',
            message=f'Erro ao salvar gravação: {str(e)}',
            timeout=5
        )
        return jsonify({"status": "erro", "mensagem": str(e)}), 500



    




@app.route('/listar_comandos_gravados', methods=['GET'])
def listar_comandos_gravados():
    try:
        arquivos = os.listdir(DIRETORIO_HISTORICO)
        jsons = [f for f in arquivos if f.endswith('.json') and f.startswith('comando_')]
        
        # Função para extrair a data do nome do arquivo
        def extrair_data(nome_arquivo):
            try:
                # Formato esperado: comando_YYYYMMDD_HHMMSS.json
                partes = nome_arquivo.split('_')
                data_str = partes[1] + '_' + partes[2].split('.')[0]
                return datetime.strptime(data_str, '%Y%m%d_%H%M%S')
            except:
                return datetime.min  # Retorna data mínima se não conseguir parsear
        
        # Ordena os arquivos por data (do mais recente para o mais antigo)
        jsons_ordenados = sorted(jsons, key=extrair_data, reverse=True)
        
        return jsonify({
            "status": "sucesso",
            "arquivos": jsons_ordenados,
            "quantidade": len(jsons_ordenados)
        })
    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e),
            "arquivos": [],
            "quantidade": 0
        }), 500







@app.route('/executar_comandos_gravados/<nome_arquivo>', methods=['GET'])
def executar_comandos_gravados(nome_arquivo):
    try:

        # Aqui manda a notificação no PC
        mensagem_formatada = formatar_nome_arquivo_notificacao(nome_arquivo)

        notification.notify(
            title='Braço Robótico em Execução',
            message=f'Comando {mensagem_formatada} está sendo executado',
            timeout=5
        )
        # Estabelece conexão serial
        ser = encontrar_arduino()
        
        caminho_arquivo = os.path.join(DIRETORIO_HISTORICO, nome_arquivo)
        
        if not os.path.exists(caminho_arquivo):
            return jsonify({"status": "erro", "mensagem": "Arquivo não encontrado"}), 404
        
        with open(caminho_arquivo, 'r') as f:
            comandos = json.load(f)
        
        if not comandos:
            return jsonify({"status": "erro", "mensagem": "Arquivo vazio"}), 400
        
        # Ordena os comandos por timestamp
        comandos_ordenados = sorted(comandos, key=lambda x: x['timestamp'])
        
        # Envia o primeiro comando
        primeiro_comando = comandos_ordenados[0]
        ser.write((json.dumps(primeiro_comando['comando']) + "\n").encode())
        print(f"[REPLAY] Enviado: {primeiro_comando}")
        ultimo_tempo = datetime.strptime(primeiro_comando['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        
        # Processa os demais comandos
        for comando in comandos_ordenados[1:]:
            # Calcula o intervalo
            tempo_atual = datetime.strptime(comando['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            delta = (tempo_atual - ultimo_tempo).total_seconds()
            
            # Espera o intervalo
            if delta > 0:
                time.sleep(delta)
            
            # Envia o comando
            ser.write((json.dumps(comando['comando']) + "\n").encode())
            print(f"[REPLAY] Enviado: {comando}")
            ultimo_tempo = tempo_atual

         # Aqui manda a notificação no PC
        mensagem_formatada = formatar_nome_arquivo_notificacao(nome_arquivo)

        notification.notify(
            title='Braço Robótico Executado com Sucesso',
            message=f'Comando {mensagem_formatada} está sendo com sucesso',
            timeout=5
        )
        
        ser.close()
        return jsonify({"status": "sucesso", "mensagem": f"Comandos do arquivo {nome_arquivo} executados com sucesso"})
    
    except Exception as e:
        if 'ser' in locals():
            ser.close()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500




def start_flask():
    app.run(port=5000, debug=False, use_reloader=False)







#=-=-=-=-=-=-=-=-=-=-= Função Estra fora do Flesk(Servidor) =-=-=-=-=-=-=-=-=-=-=



def formatar_nome_arquivo_notificacao(nome_arquivo):
    # Remove a extensão .json
    nome_sem_ext = nome_arquivo.replace('.json', '')

    # Divide pelo underline _
    partes = nome_sem_ext.split('_')

    if len(partes) >= 3:
        comando = partes[0]
        data = partes[1]
        hora = partes[2]

        # Extrai ano, mes, dia da data
        ano = data[0:4]
        mes = data[4:6]
        dia = data[6:8]

        # Extrai hora, minuto, segundo da hora
        h = hora[0:2]
        m = hora[2:4]
        s = hora[4:6]

        data_formatada = f"{dia}/{mes}/{ano} {h}:{m}:{s}"
        return f"{comando}: {data_formatada}"
    else:
        # Se o nome não está no formato esperado, retorna o nome original
        return nome_arquivo

