import threading
from braco_robotico import rum_braco
from executador_web import iniciar_executador_web
from app_flask import start_flask



# Inicia thread do Flask
thread_flask = threading.Thread(target=start_flask)
thread_flask.daemon = True
thread_flask.start()

# Inicia thread do braço robótico
thread_braco = threading.Thread(target=rum_braco)
thread_braco.daemon = True
thread_braco.start()

# Inicia app PyQt5 (bloqueante)
iniciar_executador_web()
