import os
import http.server
import socketserver
import webbrowser
import time

PORTA = 8080

def iniciar_executador_web():
    # Caminho do script atual
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    # Pasta 'web' fica no mesmo nível que a pasta do script, então sobe um nível e entra em 'web'
    diretorio_web = os.path.abspath(os.path.join(pasta_script, '..', 'web'))

    # Muda o diretório para a pasta 'web'
    os.chdir(diretorio_web)

    class TCPServerComReuso(socketserver.TCPServer):
        allow_reuse_address = True

    Handler = http.server.SimpleHTTPRequestHandler

    with TCPServerComReuso(("", PORTA), Handler) as httpd:
        url = f"http://localhost:{PORTA}"
        print(f"Servidor rodando em {url}")

        time.sleep(1)
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor interrompido manualmente.")
