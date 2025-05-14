#include <AccelStepper.h>
#include <ArduinoJson.h>  

// Motores
AccelStepper motorX(AccelStepper::DRIVER, 54, 55);
AccelStepper motorY(AccelStepper::DRIVER, 60, 61);
AccelStepper motorZ(AccelStepper::DRIVER, 46, 48);
AccelStepper motorGA(AccelStepper::DRIVER, 26, 28);// garra

// Pinos de ENABLE
#define X_ENABLE_PIN  38
#define Y_ENABLE_PIN  56
#define Z_ENABLE_PIN  62
#define GA_ENABLE_PIN 24 // garra

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
  motorX.setMaxSpeed(1000); motorX.setAcceleration(500);
  motorY.setMaxSpeed(1000); motorY.setAcceleration(500);
  motorZ.setMaxSpeed(1000); motorZ.setAcceleration(500);
  motorGA.setMaxSpeed(1000); motorGA.setAcceleration(500);

  Serial.println("Envie JSON para controlar os motores.");
}

void loop() {
  if (Serial.available()) {
    String json = Serial.readStringUntil('\n');
    StaticJsonDocument<512> doc;
    DeserializationError erro = deserializeJson(doc, json);

    if (erro) {
      Serial.println("Erro no JSON.");
      return;
    }

    moverMotor(doc, "X", motorX);
    moverMotor(doc, "Y", motorY);
    moverMotor(doc, "Z", motorZ);
    moverMotor(doc, "GA", motorGA);

    // Executa os movimentos até finalizar todos
    while (motorX.isRunning() || motorY.isRunning() || motorZ.isRunning() || motorGA.isRunning()) {
      motorX.run();
      motorY.run();
      motorZ.run();
      motorGA.run();
    }

    Serial.println("Todos os movimentos concluídos.");
  }
}

void moverMotor(JsonDocument& doc, const char* nome, AccelStepper& motor) {
  if (!doc.containsKey(nome)) return;

  const char* sentido = doc[nome]["sentido"];
  int valor = doc[nome]["passos"];

  // Converte de porcentagem (0 a 100) para passos (0 a 1600)
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


