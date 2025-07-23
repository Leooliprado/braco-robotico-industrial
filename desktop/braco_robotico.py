from inputs import get_gamepad
import json
import serial
import time
import threading
import serial.tools.list_ports

# Estado atual dos eixos
estado = {
    'X': {'sentido': 'parado', 'passos': 0},
    'Y': {'sentido': 'parado', 'passos': 0},
    'Z': {'sentido': 'parado', 'passos': 0},
    'GA': {'sentido': 'parado', 'passos': 0},
    'GA2': {'sentido': 'parado', 'agulo': 90}
}

# Função para encontrar a porta do Arduino Mega
def encontrar_arduino():
    while True:
        portas = serial.tools.list_ports.comports()
        for porta in portas:
            if "Arduino" in porta.description or "/dev/ttyUSB0" in porta.device: # Windows: 'COM3', Linux: '/dev/ttyUSB0'
                try:
                    s = serial.Serial(porta.device, 9600, timeout=1)
                    print(f"[INFO] Conectado ao Arduino em {porta.device}")
                    time.sleep(2)  # Dá tempo para o Arduino reiniciar
                    return s
                except Exception as e:
                    print(f"[ERRO] Falha ao conectar em {porta.device}: {e}")
        print("[AVISO] Arduino não encontrado. Tentando novamente em 2 segundos...")
        time.sleep(2)

# Conexão inicial com Arduino
ser = encontrar_arduino()

# Função que envia comandos continuamente
def enviar_loop():
    global ser
    while True:
        try:
            comando = {eixo: info for eixo, info in estado.items() if info['sentido'] != 'parado'}
            if comando:
                ser.write((json.dumps(comando) + "\n").encode())
                print("[ENVIO]", comando)
                with open('comando.json', 'w') as f:
                    f.write(json.dumps(comando))
            time.sleep(0.1)
        except (serial.SerialException, OSError) as e:
            print("[ERRO] Comunicação falhou. Tentando reconectar...")
            try:
                ser.close()
            except:
                pass
            ser = encontrar_arduino()

# Inicia thread de envio contínuo
threading.Thread(target=enviar_loop, daemon=True).start()

def rum_braco():
    while True:
        eventos = get_gamepad()
        for evento in eventos:
            #print(evento.code, evento.state)  # DEBUG: Mostra todos os eixos e valores
            
            if evento.ev_type == "Absolute":
                # Eixo X (analógico esquerdo horizontal - PS4: ABS_X)
                if evento.code == "ABS_X":
                    valor_normalizado = (evento.state - 128) / 128.0  # Normaliza para -1.0 a 1.0
                    if valor_normalizado > 0.5:
                        estado['X'] = {'sentido': 'frente', 'passos': int(10 * abs(valor_normalizado))}
                    elif valor_normalizado < -0.5:
                        estado['X'] = {'sentido': 'tras', 'passos': int(10 * abs(valor_normalizado))}
                    else:
                        estado['X'] = {'sentido': 'parado', 'passos': 0}
                
                # Eixo Y (analógico esquerdo vertical - PS4: ABS_Y)
                elif evento.code == "ABS_Y":
                    valor_normalizado = (evento.state - 128) / 128.0
                    if valor_normalizado > 0.5:
                        estado['Y'] = {'sentido': 'frente', 'passos': int(10 * abs(valor_normalizado))}
                    elif valor_normalizado < -0.5:
                        estado['Y'] = {'sentido': 'tras', 'passos': int(10 * abs(valor_normalizado))}
                    else:
                        estado['Y'] = {'sentido': 'parado', 'passos': 0}
                
                # Eixo Z (analógico direito horizontal - PS4: ABS_RX)
                elif evento.code == "ABS_RY":
                    valor_normalizado = (evento.state - 128) / 128.0
                    if valor_normalizado > 0.5:
                        estado['Z'] = {'sentido': 'tras', 'passos': int(10 * abs(valor_normalizado))}
                    elif valor_normalizado < -0.5:
                        estado['Z'] = {'sentido': 'frente', 'passos': int(10 * abs(valor_normalizado))}
                    else:
                        estado['Z'] = {'sentido': 'parado', 'passos': 0}
                
                # Eixo GA (analógico direito vertical - PS4: ABS_RY)
                elif evento.code == "ABS_RX":
                    valor_normalizado = (evento.state - 128) / 128.0
                    if valor_normalizado > 0.5:
                        estado['GA'] = {'sentido': 'tras', 'passos': int(10 * abs(valor_normalizado))}
                    elif valor_normalizado < -0.5:
                        estado['GA'] = {'sentido': 'frente', 'passos': int(10 * abs(valor_normalizado))}
                    else:
                        estado['GA'] = {'sentido': 'parado', 'passos': 0}

            
                # R2 analógico (ABS_RZ): controla diretamente o ângulo
                elif evento.code == "ABS_RZ":
                    valor = evento.state / 255.0
                    angulo = int((1 - valor) * 180)  # R2 controla diretamente o ângulo
                    estado['GA2']['agulo'] = max(0, min(angulo, 180))
                    estado['GA2']['sentido'] = 'ajustando'
                    print(f"GA2 (servo) ângulo ajustado: {estado['GA2']['agulo']} graus")



            elif evento.ev_type == "Key":
                if evento.code == "BTN_TR" and evento.state == 1:
                    print("R1 pressionado")
                elif evento.code == "BTN_TL" and evento.state == 1:
                    print("L1 pressionado")
