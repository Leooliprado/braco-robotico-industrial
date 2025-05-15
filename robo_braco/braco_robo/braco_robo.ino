#include <AccelStepper.h>
#include <ArduinoJson.h>  

// Motores
AccelStepper motorX(AccelStepper::DRIVER, 54, 55);
AccelStepper motorY(AccelStepper::DRIVER, 60, 61);
AccelStepper motorZ(AccelStepper::DRIVER, 46, 48);
AccelStepper motorGA(AccelStepper::DRIVER, 26, 28);

// Pinos de ENABLE
#define X_ENABLE_PIN  38
#define Y_ENABLE_PIN  56
#define Z_ENABLE_PIN  62
#define GA_ENABLE_PIN 24

String bufferSerial = "";

void setup() {
  Serial.begin(9600);

  pinMode(X_ENABLE_PIN, OUTPUT);
  pinMode(Y_ENABLE_PIN, OUTPUT);
  pinMode(Z_ENABLE_PIN, OUTPUT);
  pinMode(GA_ENABLE_PIN, OUTPUT);

  digitalWrite(X_ENABLE_PIN, LOW);
  digitalWrite(Y_ENABLE_PIN, LOW);
  digitalWrite(Z_ENABLE_PIN, LOW);
  digitalWrite(GA_ENABLE_PIN, LOW);

  // Configurações de movimento
  motorX.setMaxSpeed(1000); motorX.setAcceleration(900);
  motorY.setMaxSpeed(1000); motorY.setAcceleration(900);
  motorZ.setMaxSpeed(1000); motorZ.setAcceleration(900);
  motorGA.setMaxSpeed(1000); motorGA.setAcceleration(900);

  Serial.println("Envie JSON para controlar os motores.");
}

void loop() {
  // Chamada constante para garantir movimento contínuo
  motorX.run();
  motorY.run();
  motorZ.run();
  motorGA.run();

  // Monta o buffer do JSON linha por linha
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      StaticJsonDocument<512> doc;
      DeserializationError erro = deserializeJson(doc, bufferSerial);

      if (erro) {
        Serial.println("Erro no JSON.");
      } else {
        moverMotor(doc, "X", motorX);
        moverMotor(doc, "Y", motorY);
        moverMotor(doc, "Z", motorZ);
        moverMotor(doc, "GA", motorGA);
        Serial.println("Comando recebido.");
      }
      bufferSerial = "";  // limpa buffer
    } else {
      bufferSerial += c;
    }
  }
}

void moverMotor(JsonDocument& doc, const char* nome, AccelStepper& motor) {
  if (!doc.containsKey(nome)) return;

  const char* sentido = doc[nome]["sentido"];
  int valor = doc[nome]["passos"];

  int passos = constrain(valor, 0, 100) * 16;

  if (strcmp(sentido, "tras") == 0) {
    passos = -passos;
  }

  motor.moveTo(motor.currentPosition() + passos);

  Serial.print("Motor ");
  Serial.print(nome);
  Serial.print(" -> ");
  Serial.print(sentido);
  Serial.print(" ");
  Serial.print(abs(passos));
  Serial.println(" passos");
}


/*


{
  "X": {"sentido": "frente", "passos": 50},
  "Y": {"sentido": "tras", "passos": 25},
  "Z": {"sentido": "frente", "passos": 75},
  "GA": {"sentido": "tras", "passos": 100}
}


*/


