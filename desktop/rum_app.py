import threading
from braco_robotico import rum_braco
from executador_web import iniciar_executador_web

# Cria threads para cada função
thread_braco = threading.Thread(target=rum_braco)
thread_web = threading.Thread(target=iniciar_executador_web)

# Inicia as threads
thread_braco.start()
thread_web.start()

# Opcional: esperar as threads terminarem (bloqueia aqui)
thread_braco.join()
thread_web.join()
