from inputs import get_gamepad
import json
import serial
import time
import threading

# Inicializa porta serial
ser = serial.Serial('/dev/ttyUSB0', 9600) # Windows: 'COM3', Linux: '/dev/ttyUSB0'
time.sleep(2)

# Estado atual dos eixos
estado = {
    'X': {'sentido': 'parado', 'passos': 0},
    'Y': {'sentido': 'parado', 'passos': 0},
    'Z': {'sentido': 'parado', 'passos': 0},
    'GA': {'sentido': 'parado', 'passos': 0}
}

# Função que envia comandos continuamente
def enviar_loop():
    while True:
        comando = {eixo: info for eixo, info in estado.items() if info['sentido'] != 'parado'}
        if comando:
            ser.write((json.dumps(comando) + "\n").encode())
            print("Enviado:", comando)
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
                        estado['Y'] = {'sentido': 'tras', 'passos': int(10 * abs(valor_normalizado))}
                    elif valor_normalizado < -0.5:
                        estado['Y'] = {'sentido': 'frente', 'passos': int(10 * abs(valor_normalizado))}
                    else:
                        estado['Y'] = {'sentido': 'parado', 'passos': 0}
                
                # Eixo Z (analógico direito horizontal - PS4: ABS_RX)
                elif evento.code == "ABS_RX":
                    valor_normalizado = (evento.state - 128) / 128.0
                    if valor_normalizado > 0.5:
                        estado['Z'] = {'sentido': 'frente', 'passos': int(10 * abs(valor_normalizado))}
                    elif valor_normalizado < -0.5:
                        estado['Z'] = {'sentido': 'tras', 'passos': int(10 * abs(valor_normalizado))}
                    else:
                        estado['Z'] = {'sentido': 'parado', 'passos': 0}
                
                # Eixo GA (analógico direito vertical - PS4: ABS_RY)
                elif evento.code == "ABS_RY":
                    valor_normalizado = (evento.state - 128) / 128.0
                    if valor_normalizado > 0.5:
                        estado['GA'] = {'sentido': 'tras', 'passos': int(10 * abs(valor_normalizado))}
                    elif valor_normalizado < -0.5:
                        estado['GA'] = {'sentido': 'frente', 'passos': int(10 * abs(valor_normalizado))}
                    else:
                        estado['GA'] = {'sentido': 'parado', 'passos': 0}
            
            #R1 L1
            elif evento.ev_type == "Key":
                if evento.code == "BTN_TR" and evento.state == 1:  # Gatilho R1
                    print("Botão R1 pressionado")
                elif evento.code == "BTN_TL" and evento.state == 1:  # Gatilho L1
                    print("Botão L1 pressionado")
            

      # Gatilho L2 (ABS_Z)
            if evento.code == "BTN_TR2" and evento.state == 1:
                print("R2 (digital) pressionado")
            elif evento.code == "ABS_RZ":
                valor = evento.state / 255.0
                if valor > 0.2:
                    print(f"R2 (analógico) pressionado com intensidade: {valor:.2f}")

           # Gatilho L2 (ABS_Z)
            if evento.ev_type == "Key" and evento.code == "BTN_TL2" and evento.state == 1:
                print("Botão L2 (digital) pressionado")

            elif evento.ev_type == "Absolute" and evento.code == "ABS_Z":
                valor = evento.state / 255.0
                if valor > 0.2:
                    print(f"L2 (analógico) pressionado com intensidade: {valor:.2f}")


            
