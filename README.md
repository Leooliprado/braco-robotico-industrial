
# 🤖 braco-robotico-industrial

Sistema de controle para braço robótico industrial utilizando um controle de videogame como joystick. Os comandos são enviados via JSON para um Arduino Mega que controla motores de passo, com visualização em tempo real via interface web.

---

## 📦 Clonar o Projeto

Clone o repositório com o comando abaixo:

```bash
git clone https://github.com/Leooliprado/braco-robotico-industrial.git
````

---

## 🚀 Como Executar

Após clonar o repositório:

### 💻 Windows

Clique duas vezes no arquivo:

```
start_robot.bat
```

### 🐧 Linux

Dê permissão de execução e execute:

```bash
chmod +x start_robot.sh
./start_robot.sh
```

> Esses scripts iniciam automaticamente o monitoramento do controle e o servidor web.

---

## 🎮 Funcionalidade

* Controle dos eixos X, Y, Z e GA via gamepad (ex: controle PS4).
* Comunicação serial com Arduino via JSON.
* Visualização dos comandos em tempo real por navegador.
* Visualização da câmera ao vivo.

---

## 🌐 Interface Web

Acesse pelo navegador:

```
http://localhost:8080
```

* **Comando Atual:** Exibe o JSON enviado ao Arduino.
* **Câmera Ao Vivo:** Mostra o stream da câmera (ex: `http://192.168.15.12:81/stream`).

---

## 🔌 Hardware Recomendado

* Arduino Mega 2560
* Drivers A4988 ou similares
* Motores de passo
* Controle de videogame (USB)
* Câmera IP (opcional)
* Fonte externa adequada para motores

---

## 📘 Exemplo de Comando Enviado

```json
{
  "X": {"sentido": "frente", "passos": 50},
  "Y": {"sentido": "tras", "passos": 25},
  "Z": {"sentido": "frente", "passos": 75},
  "GA": {"sentido": "tras", "passos": 100}
}
```

---

## 👨‍💻 Autores

Desenvolvido por \Leonardo De Oliveira Prado e Felipe Silveira Volpe.

---

## 📝 Licença

Este projeto é de uso livre, inclusive para modificações, **desde que o autor principal seja mencionado** nos créditos de qualquer versão derivada.




---


