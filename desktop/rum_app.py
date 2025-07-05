from braco_robotico import rum_braco
from executador_web import iniciar_executador_web
import threading

# Cria a thread para o braço robótico como daemon
thread_braco = threading.Thread(target=rum_braco)
thread_braco.daemon = True

# Inicia a thread
thread_braco.start()

# Na thread principal, roda o app PyQt5
iniciar_executador_web()

# Não precisa de join, pois daemon para junto com o processo

