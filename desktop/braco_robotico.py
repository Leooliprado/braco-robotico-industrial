from inputs import get_gamepad
import json
import serial
import time
import threading



# Inicializa porta serial
ser = serial.Serial('/dev/ttyUSB0', 9600) # Windows: 'COM3', Linux: '/dev/ttyUSB0'
time.sleep(2)

# Estado atual dos eixos
# Estado atual
estado = {
    'X': {'sentido': 'parado', 'passos': 0},
    'Y': {'sentido': 'parado', 'passos': 0},
    'Z': {'sentido': 'parado', 'passos': 0},
    'GA': {'sentido': 'parado', 'passos': 0},
    'GA2': {'sentido': 'parado', 'agulo': 90}  # Servo começa no meio
}

# Função que envia comandos continuamente
def enviar_loop():
    while True:
        comando = {eixo: info for eixo, info in estado.items() if info['sentido'] != 'parado'}
        if comando:
            ser.write((json.dumps(comando) + "\n").encode())
            print("Enviado:", comando)
               # Escreve o comando em um arquivo txt
            with open('comando.json', 'w') as f:
                f.write(json.dumps(comando))
            print("Comando salvo:", comando)
        time.sleep(0.1)

# Inicia thread para envio contínuo
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



                # # L2 analógico (ABS_Z): diminui ângulo do servo
                # elif evento.code == "ABS_Z":
                #     valor = evento.state / 255.0
                #     if valor > 0.1:
                #         novo_angulo = int(estado['GA2']['agulo'] - valor * 5)
                #         estado['GA2']['agulo'] = max(novo_angulo, 0)
                #         estado['GA2']['sentido'] = 'menos'
                #         print(f"GA2 diminuindo para {estado['GA2']['agulo']} graus")
                #     else:
                #         estado['GA2']['sentido'] = 'parado'

            elif evento.ev_type == "Key":
                if evento.code == "BTN_TR" and evento.state == 1:
                    print("R1 pressionado")
                elif evento.code == "BTN_TL" and evento.state == 1:
                    print("L1 pressionado")
