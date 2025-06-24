# <img src="https://img.icons8.com/emoji/48/robot-emoji.png" width="30"/> Braço Robotico Industrial

Sistema de controle para braço robótico industrial utilizando um controle de videogame como joystick. Os comandos são enviados via JSON para um Arduino Mega que controla motores de passo, com visualização em tempo real via interface web.

---

## <img src="https://img.icons8.com/fluency/48/download.png" width="28"/> Clonar o Projeto

Clone o repositório com o comando abaixo:

```bash
git clone https://github.com/Leooliprado/braco-robotico-industrial.git
````

---

## <img src="https://img.icons8.com/fluency/48/play.png" width="28"/> Como Executar

Após clonar o repositório:

### <img src="https://img.icons8.com/fluency/48/windows-10.png" width="20"/> Windows

Clique duas vezes no arquivo:

```
start_robot.bat
```

### <img src="https://img.icons8.com/color/48/linux.png" width="20"/> Linux

Dê permissão de execução e execute:

```bash
chmod +x start_robot.sh
./start_robot.sh
```

> Esses scripts iniciam automaticamente o monitoramento do controle e o servidor web.

---

## <img src="https://img.icons8.com/fluency/48/controller.png" width="28"/> Funcionalidade


* Controle dos eixos X, Y, Z e GA via gamepad (controle de PS4).
* Comunicação serial com Arduino via JSON.
* Visualização dos comandos em tempo real por navegador.
* Visualização da câmera ao vivo.

---

## <img src="https://img.icons8.com/fluency/48/internet.png" width="28"/> Interface Web

Acesse pelo navegador:

```
http://localhost:8080
```

* **Comando Atual:** Exibe o JSON enviado ao Arduino.
* **Câmera Ao Vivo:** Exibe o stream da câmera ESP32-CAM (usando o código padrão de demonstração da webcam), exemplo de URL: `http://192.168.15.12:81/stream`.


---

## <img src="https://img.icons8.com/fluency/48/electrical.png" width="28"/> Hardware Recomendado

* Arduino Mega 2560
* Drivers A4988 ou similares
* Motores de passo
* Controle de videogame USB (DualShock 4 - PS4)
* Câmera IP (opcional)
* Fonte externa adequada para motores

---

## <img src="https://img.icons8.com/fluency/48/source-code.png" width="28"/> Exemplo de Comando Enviado

```json
{
  "X": {"sentido": "frente", "passos": 50},
  "Y": {"sentido": "tras", "passos": 25},
  "Z": {"sentido": "frente", "passos": 75},
  "GA": {"sentido": "tras", "passos": 100}
}
```

---

## <img src="https://img.icons8.com/fluency/48/conference-background-selected.png" width="28"/> Autores

Desenvolvido por **Leonardo De Oliveira Prado** e **Felipe Silveira Volpe**.

---

## <img src="https://img.icons8.com/fluency/48/privacy.png" width="28"/> Licença

Este projeto é de uso livre, inclusive para modificações, **desde que o autor principal seja mencionado** nos créditos de qualquer versão derivada.

---
