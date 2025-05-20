import http.server
import socketserver
import os
import webbrowser  # <- Importa para abrir navegador automaticamente
import time



PORTA = 8000

def iniciar_executador_web():
    # Define o diretório do projeto como raiz dos arquivos servidos
    diretorio = os.path.dirname(os.path.abspath(__file__))
    os.chdir(diretorio)

    class TCPServerComReuso(socketserver.TCPServer):
        allow_reuse_address = True  # Permite reusar a porta mesmo após encerramento

    Handler = http.server.SimpleHTTPRequestHandler

    with TCPServerComReuso(("", PORTA), Handler) as httpd:
        url = f"http://localhost:{PORTA}"
        print(f"Servidor rodando em {url}")
        
        # Pequeno delay para garantir que o servidor está pronto
        time.sleep(1)
        
        # Abre o navegador na URL do servidor
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor interrompido manualmente.")
