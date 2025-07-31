#include <AccelStepper.h>
#include <ArduinoJson.h>
#include <Servo.h>

// Motores
AccelStepper motorX(AccelStepper::DRIVER, 54, 55);
AccelStepper motorY(AccelStepper::DRIVER, 60, 61);
AccelStepper motorZ(AccelStepper::DRIVER, 46, 48);
AccelStepper motorGA(AccelStepper::DRIVER, 26, 28);

AccelStepper motorGA2(AccelStepper::HALF4WIRE, 4, 6, 5, 11);




// Pinos de ENABLE
#define X_ENABLE_PIN 38
#define Y_ENABLE_PIN 56
#define Z_ENABLE_PIN 62
#define GA_ENABLE_PIN 24

// limete da GA e o X para não estragar o fios
//150° no codigo. no robo 150°
#define MAX_PASSOS_GA 853 
#define MIN_PASSOS_GA -853
// 360° no codigo. com a engrenagem planetaria é 180°
#define MAX_PASSOS_X 2048  
#define MIN_PASSOS_X -2048

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
  motorX.setMaxSpeed(1000);
  motorX.setAcceleration(900);
  motorY.setMaxSpeed(1000);
  motorY.setAcceleration(900);
  motorZ.setMaxSpeed(1000);
  motorZ.setAcceleration(900);
  motorGA.setMaxSpeed(1000);
  motorGA.setAcceleration(900);

  motorGA2.setMaxSpeed(350);      // velocidade máxima
  motorGA2.setAcceleration(150);  // aceleração 






  Serial.println("Envie JSON para controlar os motores e o servo.");
}

void loop() {
  // Motores
  motorX.run();
  motorY.run();
  motorZ.run();
  motorGA.run();

  motorGA2.run();
  // motorGA2.moveTo(2048); // Vai girar 1 volta para frente

  // Recebe JSON
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
        moverMotorGA2(doc);
        Serial.println("Comando recebido.");
      }
      bufferSerial = "";
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

  long novaPosicao = motor.currentPosition() + passos;

  if (strcmp(nome, "GA") == 0) {
    if (novaPosicao > MAX_PASSOS_GA) {
      novaPosicao = MAX_PASSOS_GA;
      Serial.println("GA atingiu o limite de +180°");
    } else if (novaPosicao < MIN_PASSOS_GA) {
      novaPosicao = MIN_PASSOS_GA;
      Serial.println("GA atingiu o limite de -180°");
    }
    motor.moveTo(novaPosicao);
  } else if (strcmp(nome, "X") == 0) {
      if (novaPosicao > MAX_PASSOS_X) {
        novaPosicao = MAX_PASSOS_X;
        Serial.println("X atingiu o limite de +350°");
      } else if (novaPosicao < MIN_PASSOS_X) {
        novaPosicao = MIN_PASSOS_X;
        Serial.println("X atingiu o limite de -350°");
      }
      motor.moveTo(novaPosicao);
  } else {
    motor.moveTo(novaPosicao);
  }

  Serial.print("Motor ");
  Serial.print(nome);
  Serial.print(" -> ");
  Serial.print(sentido);
  Serial.print(" ");
  Serial.print(abs(passos));
  Serial.println(" passos");
}




void moverMotorGA2(JsonDocument& doc) {
  if (!doc.containsKey("GA2")) return;

  const char* sentido = doc["GA2"]["sentido"];
  int valor = doc["GA2"]["passos"];
  int passos = constrain(valor, 0, 100) * 8; // aumente a multiplicação para mais força

  if (strcmp(sentido, "tras") == 0) passos = -passos;

  motorGA2.moveTo(motorGA2.currentPosition() + passos);

  Serial.print("Motor GA2 -> ");
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
  "GA2": {"sentido": "tras", "agulo": 100}
}


*/
