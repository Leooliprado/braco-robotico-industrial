import sys
import os
import threading
import http.server
import socketserver
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from functools import partial 

# from PyQt5.QtWebEngineWidgets import QWebEngineProfile


PORTA = 8080

class TCPServerComReuso(socketserver.TCPServer):
    allow_reuse_address = True

class ServidorThread(threading.Thread):
    def __init__(self, porta):
        super().__init__()
        self.porta = porta
        self.httpd = None

    def run(self):
        # Caminho do script atual
        pasta_script = os.path.dirname(os.path.abspath(__file__))
        diretorio_web = os.path.abspath(os.path.join(pasta_script, '..', 'web'))

        # NÃO use mais os.chdir(diretorio_web)

        # Define o handler com o diretório da web corretamente
        Handler = partial(http.server.SimpleHTTPRequestHandler, directory=diretorio_web)

        with TCPServerComReuso(("", self.porta), Handler) as httpd:
            self.httpd = httpd
            print(f"Servidor rodando em http://localhost:{self.porta}")
            httpd.serve_forever()

    def stop(self):
        if self.httpd:
            print("Parando servidor HTTP...")
            self.httpd.shutdown()

class MainWindow(QMainWindow):
    def __init__(self, servidor_thread):
        super().__init__()
        self.servidor_thread = servidor_thread

        self.setWindowTitle("Braço Robotico Industrial")
        self.setGeometry(100, 100, 800, 600)# tamanho da janela sem maximizar
        self.showMaximized()#deicha em tela cheia (maximizar)

        # Limpa cookies e cache
        # profile = QWebEngineProfile.defaultProfile()
        # profile.cookieStore().deleteAllCookies()
        # profile.clearHttpCache()



        view = QWebEngineView()
        view.load(QUrl(f"http://localhost:{PORTA}/index.html"))
        self.setCentralWidget(view)

    def closeEvent(self, event):
        self.servidor_thread.stop()
        event.accept()

def iniciar_executador_web():
    """Função para iniciar o servidor + janela"""
    servidor_thread = ServidorThread(PORTA)
    servidor_thread.start()

    app = QApplication(sys.argv)
    janela = MainWindow(servidor_thread)
    janela.show()
    sys.exit(app.exec_())
