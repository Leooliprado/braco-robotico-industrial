# <img src="https://img.icons8.com/emoji/48/robot-emoji.png" width="30"/> Braço Robotico Industrial

Sistema de controle para braço robótico industrial utilizando um controle de videogame como joystick. Os comandos são enviados via JSON para um Arduino Mega, que controla motores de passo, com visualização em tempo real por meio de uma interface. Os movimentos também podem ser gravados e reproduzidos posteriormente, permitindo a automação do braço robótico, que executa os movimentos de forma autônoma conforme os comandos programados. O sistema permite que o braço seja controlado manualmente pelo joystick ou funcione sozinho. O projeto utiliza um Arduino Mega com um shield de impressora 3D acoplado.

---

## <img src="https://img.icons8.com/fluency/48/download.png" width="28"/> Clonar o Projeto

Clone o repositório com o comando abaixo:

```bash
git clone https://github.com/Leooliprado/braco-robotico-industrial.git
```

---

## 📦 Dependências (requirements.txt)

Todas as dependências necessárias já estão listadas no arquivo `requirements.txt` incluído no projeto:

```txt
pyserial
flask
flask-cors
inputs
pyqt5
pyqtwebengine
plyer
````

**Passo a passo recomendado:**

1. Navegue até a pasta `desktop` do projeto:

```bash
cd desktop
```

2. Crie o ambiente virtual dentro desta pasta:

```bash
python -m venv venv
```

3. Ative o ambiente virtual:

* **Windows:**

  ```bash
  venv\Scripts\activate
  ```

* **Linux / macOS:**

  ```bash
  source venv/bin/activate
  ```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

> Isso vai instalar as dependências para a interface PyQt5, o motor WebEngine para exibir HTML, a biblioteca para capturar eventos do controle (inputs) e a biblioteca para comunicação serial com Arduino.

---


## <img src="https://img.icons8.com/fluency/48/play.png" width="28"/> Como Executar

Após clonar o repositório e instalar todas as bibliotecas:

### <img src="https://img.icons8.com/fluency/48/windows-10.png" width="20"/> Windows

No código, altere a verificação da porta serial para:

```python
if "Arduino" in porta.description or "/dev/ttyUSB0" in porta.device:
    # Windows: 'COM3', Linux: '/dev/ttyUSB0'
```

⚠️ **Atenção:** pode haver problemas com o sistema de notificações no Windows, portanto pode ser necessário fazer ajustes específicos.
Ainda não realizei testes no Windows, então seria importante validar.
Se você testar e conseguir fazer funcionar, pode me contatar pelo e-mail disponível no meu perfil do GitHub para compartilhar a modificação.

> O objetivo principal do projeto é funcionar corretamente no Linux, por ser o sistema prioritário em projetos de escala real e industrial. O Linux oferece maior flexibilidade, estabilidade e suporte para aplicações desse tipo.

Para executar no Windows, clique duas vezes no arquivo:

```
start_robot.bat
```

---

### <img src="https://img.icons8.com/color/48/linux.png" width="20"/> Linux

No Linux, existem **duas formas** de executar:


### **1) Pelo código-fonte (modo desenvolvimento)**


#### ➤  Usando o script de inicialização:

Dê permissão de execução e execute:

```bash
chmod +x start_robot.sh
./start_robot.sh
```

> Este script inicia automaticamente o monitoramento do controle e abre o aplicativo desktop que renderiza a interface HTML usando PyQt5.

---

### **2) Diretamente pelo aplicativo desktop:**

Ative o ambiente virtual (caso ainda não tenha feito):

```bash
source venv/bin/activate
```

Instale o **Nuitka**, se ainda não estiver instalado:

```bash
pip install nuitka
```

Rode o aplicativo com:

```bash
nuitka rum_app.py
```


No Linux, basta clicar no arquivo:

```
rum_app.bin
```

E, para facilitar, você também pode criar um **atalho na área de trabalho** como este:

```ini
[Desktop Entry]
Name=Braço Robótico Industrial
Comment=Aplicativo para controlar um braço robótico industrial com Arduino Mega via comunicação serial e controle de PS4.
Exec=/home/user/Documentos/GitHub/braco-robotico-industrial/desktop/rum_app.bin
Icon=/home/user/Documentos/GitHub/braco-robotico-industrial/desktop/icons/icon.png
Terminal=false
Type=Application
Categories=Robotics;Engineering;Electronics;
```

> Salve esse conteúdo em um arquivo chamado `braco.desktop` na área de trabalho e dê permissão de execução para o atalho:

```bash
chmod +x ~/Área\ de\ Trabalho/braco.desktop
```

Assim, você poderá iniciar o sistema com um **clique**.

---

## ❗ Erros Comuns e Soluções

### 🚫 Erro de Permissão no Arduino

```
[ERRO] Falha ao conectar em /dev/ttyUSB0: [Errno 13] Permission denied: '/dev/ttyUSB0'
```

**Causa:** Seu usuário não tem permissão para acessar a porta serial do Arduino.
**Solução:**

```bash
sudo usermod -aG dialout seu_user
```

Depois **faça logout/login** (ou reinicie o PC).


---

### 🚫 Erro ao abrir janela do Qt (plugin `xcb`)

```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized.
```

**Causa:** O Qt (PyQt5) não encontra as dependências do plugin gráfico `xcb`.
**Solução:** Instale as bibliotecas necessárias:

```bash
sudo apt update
sudo apt install libxcb-xinerama0 libxcb-xinerama0-dev \
                 libx11-xcb1 libx11-xcb-dev \
                 libglu1-mesa libglu1-mesa-dev \
                 libxrender1 libxi6 libxrandr2 \
                 libxss1 libxtst6
```




---

## ⚙️ Montagem do Braço Robótico e Programação

1. **Carregar o código no Arduino**
   O código do braço robótico está no diretório:

   ```bash
   robo_braco/braco_robo/braco_robo.ino
   ```

   Abra esse arquivo na **Arduino IDE** e faça o upload para a placa **Arduino Mega 2560**.

---

2. **Montagem e conexões**

   * Utilize a placa **Arduino Mega 2560 R3** junto com a **RAMPS 1.4** como controlador.
   * Conecte o **módulo do motor de passo 28BYJ-48** com o **driver ULN2003** (responsável pela garra).
   * Com um **jumper**, feche o curto entre o **V5** e o **VCC**, conforme a imagem abaixo:

  ![Conexão do ULN2003 com Arduino](https://github.com/Leooliprado/braco-robotico-industrial/blob/main/img/1.jpeg)
  
   * Faça as ligações dos pinos conforme listado:

     * **Pinos digitais:** 4, 6, 5 e 11
     * **GND do driver** → **GND do Arduino Mega 2560**
     * **VCC positivo do driver** → **Fonte externa de 5V**

   *(imagem aqui)*

---

3. **Fonte de alimentação**
   Recomenda-se utilizar uma **fonte externa estável**.
   No meu caso, estou usando um **diminuidor de tensão (step-down)**, que converte **12V para 5V**.

   Dessa forma, o Arduino Mega controla os motores de passo com segurança, evitando sobrecarga na própria placa.

   *(imagem aqui)*

---

4. **Motores Nema 17 (eixos principais)**

   * Os outros **4 motores de passo Nema 17** são conectados diretamente na **RAMPS 1.4**, cada um com seu respectivo **driver A4988**.
   * A RAMPS já possui conectores dedicados para os eixos: **X, Y, Z, GA e GA2**.
   * Cada driver A4988 deve estar corretamente encaixado na RAMPS, respeitando a orientação.

   *(imagem aqui)*

---

Assim, você terá:

* **Motores Nema 17** (eixos principais) controlados pela RAMPS + A4988
* **Motor 28BYJ-48 (garra)** controlado pelo ULN2003 conectado diretamente ao Arduino

---



## <img src="https://img.icons8.com/fluency/48/controller.png" width="28"/> Funcionalidade

* Controle dos eixos X, Y, Z , GA e GA2 via gamepad (controle de PS4).
* Comunicação serial com Arduino via JSON.
* Visualização dos comandos em tempo real no aplicativo desktop.
* Visualização da câmera ao vivo.

---


## <img src="https://img.icons8.com/fluency/48/electrical.png" width="28"/> Hardware Recomendado

* Arduino Mega 2560
* Drivers A4988 ou similares
* Motores de passo nema 17
* Um motor de Passo 28BYJ-48 com o driver ULN2003
* Controle de videogame USB (DualShock 4 - PS4)
* ESP32-CAM (opcional)
* Fonte externa adequada para motores

---

## <img src="https://img.icons8.com/fluency/48/source-code.png" width="28"/> Exemplo de Comando Enviado

```json
{
  "X": {"sentido": "frente", "passos": 50},
  "Y": {"sentido": "tras", "passos": 25},
  "Z": {"sentido": "frente", "passos": 75},
  "GA": {"sentido": "tras", "passos": 100},
  "GA2": {"sentido": "tras", "agulo": 100}
}
```

---

## <img src="https://img.icons8.com/fluency/48/robot.png" width="28"/> Estrutura do Braço Robótico

* [Projeto Original do Braço Robótico](https://www.printables.com/model/132260-we-r24-six-axis-robot-arm/files)
  *Descrição:* Projeto base usado como inspiração.

* [Projeto modificado que usei no meu projeto](https://www.thingiverse.com/thing:5672870)
  *Descrição:* Adaptação e melhorias feitas a partir do projeto original.

---

## <img src="https://img.icons8.com/fluency/48/conference-background-selected.png" width="28"/> Autores

Desenvolvido por  
**[Leonardo De Oliveira Prado (Leooliprado)](https://github.com/Leooliprado)** e  
**[Felipe Silveira Volpe (FelipeVolpe)](https://github.com/FelipeVolpe)**

---



