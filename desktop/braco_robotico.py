import serial
import serial.tools.list_ports
import json
import pygame
import time
import sys

# Detecta portas disponíveis
ports = list(serial.tools.list_ports.comports())
porta_serial = None

for port in ports:
    if "ttyUSB" in port.device or "ttyACM" in port.device:
        porta_serial = port.device
        break

if not porta_serial:
    print("Nenhum dispositivo serial encontrado (ex: /dev/ttyUSB0 ou /dev/ttyACM0).")
    sys.exit(1)

# Tenta abrir a porta
try:
    ser = serial.Serial(porta_serial, 9600)
    time.sleep(2)
except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial {porta_serial}: {e}")
    sys.exit(1)

    
# Inicialização do PyGame e joystick
pygame.init()
screen = pygame.display.set_mode((400, 180))
pygame.display.set_caption("Controle Braço Robótico PS2 - Modo Analógico")

if pygame.joystick.get_count() == 0:
    print("Nenhum joystick encontrado!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Variáveis de controle
passo_base = 10
passo_rapido_mult = 3
ultimo_envio = 0
intervalo_envio = 0.1  # 100ms
estado_anterior = {}

eixos = {
    'X': {'sentido': 'parado', 'passos': 0},
    'Y': {'sentido': 'parado', 'passos': 0},
    'Z': {'sentido': 'parado', 'passos': 0},
    'GA': {'sentido': 'parado', 'passos': 0}
}

def enviar_comando():
    global ultimo_envio, estado_anterior
    agora = time.time()
    if agora - ultimo_envio < intervalo_envio:
        return

    comando = {eixo: info for eixo, info in eixos.items() if info['sentido'] != 'parado'}
    if comando:
        json_comando = json.dumps(comando)
        print(f"Enviando: {json_comando}")
        ser.write((json_comando + '\n').encode())

    estado_anterior = {eixo: info.copy() for eixo, info in eixos.items()}
    ultimo_envio = agora

# Mapeamento dos controles
BOTOES = {
    'TRIANGULO': 0, 'CIRCULO': 1, 'XIS': 2, 'QUADRADO': 3,
    'L1': 4, 'R1': 5, 'L2': 6, 'R2': 7,
    'SELECT': 8, 'START': 9, 'ANALOGICO_ESQ': 10, 'ANALOGICO_DIR': 11,
    'CIMA': 12, 'BAIXO': 13, 'ESQUERDA': 14, 'DIREITA': 15
}

AXIS = {
    'ANALOGICO_ESQ_H': 0, 'ANALOGICO_ESQ_V': 1,
    'ANALOGICO_DIR_H': 2, 'ANALOGICO_DIR_V': 3
}

analogico_ativo = {'X': False, 'Y': False}

print("Controle com PS2 - Modo Analógico")
print("Analógicos: Movimento contínuo")
print("Botões: Comandos discretos")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == BOTOES['START']:
                running = False
            elif event.button == BOTOES['L1']:
                passo_base = max(1, passo_base - 1)
                print(f"Passo base diminuído: {passo_base}")
            elif event.button == BOTOES['R1']:
                passo_base = min(100, passo_base + 1)
                print(f"Passo base aumentado: {passo_base}")

    modo_rapido = joystick.get_button(BOTOES['R2'])
    passo_atual = passo_base * passo_rapido_mult if modo_rapido else passo_base

    for eixo in eixos:
            # Resetar eixos antes de ler novos valores
        for eixo in eixos:
            eixos[eixo]['sentido'] = 'parado'
            eixos[eixo]['passos'] = 0

    # Analógicos
    deadzone = 0.3

    # Esquerdo - Eixos X e Y
    axis_x = joystick.get_axis(AXIS['ANALOGICO_ESQ_H'])
    axis_y = joystick.get_axis(AXIS['ANALOGICO_ESQ_V'])

    if abs(axis_x) > deadzone:
        eixos['X']['sentido'] = 'frente' if axis_x > 0 else 'tras'
        eixos['X']['passos'] = passo_atual

    if abs(axis_y) > deadzone:
        eixos['Y']['sentido'] = 'tras' if axis_y > 0 else 'frente'
        eixos['Y']['passos'] = passo_atual

    # Direito - Eixo Z
    axis_z = joystick.get_axis(AXIS['ANALOGICO_DIR_V'])

    if abs(axis_z) > deadzone:
        eixos['Z']['sentido'] = 'tras' if axis_z > 0 else 'frente'
        eixos['Z']['passos'] = passo_atual


    # Botões (Z e GA)
    if joystick.get_button(BOTOES['TRIANGULO']):
        eixos['Z']['sentido'] = 'frente'
        eixos['Z']['passos'] = passo_atual
    elif joystick.get_button(BOTOES['XIS']):
        eixos['Z']['sentido'] = 'tras'
        eixos['Z']['passos'] = passo_atual

    if joystick.get_button(BOTOES['CIRCULO']):
        eixos['GA']['sentido'] = 'frente'
        eixos['GA']['passos'] = passo_atual
    elif joystick.get_button(BOTOES['QUADRADO']):
        eixos['GA']['sentido'] = 'tras'
        eixos['GA']['passos'] = passo_atual

    enviar_comando()

    # Interface
    screen.fill((240, 240, 240))
    font = pygame.font.SysFont('Arial', 22)
    texto_passo = font.render(f"Passo base: {passo_base}", True, (0, 0, 0))
    texto_passo_real = font.render(f"Passo atual: {passo_atual}", True, (0, 0, 0))
    texto_rapido = font.render(f"Modo rápido: {'Sim' if modo_rapido else 'Não'}", True, (0, 0, 0))
    texto_x = font.render(f"X: {eixos['X']['sentido']}", True, (0, 0, 0))
    texto_y = font.render(f"Y: {eixos['Y']['sentido']}", True, (0, 0, 0))

    screen.blit(texto_passo, (20, 10))
    screen.blit(texto_passo_real, (20, 35))
    screen.blit(texto_rapido, (20, 60))
    screen.blit(texto_x, (20, 90))
    screen.blit(texto_y, (20, 115))
    pygame.display.flip()

    clock.tick(30)

pygame.quit()
ser.close()
