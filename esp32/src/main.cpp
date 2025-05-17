#include "DHT.h"

#define BTN_P 13 // Botão Fósforo
#define BTN_K 14 // Botão Potássio
#define LDR 34 // LDR Ph
#define DHTPIN 23 // Pino Sensor de umidade
#define DHTTYPE DHT22
#define RELE_PIN 17 // Pino de acionamento do Relé

DHT dht(DHTPIN, DHTTYPE);

float umidade, phRaw, ph;
bool temFosforo, temPotassio;

// Constantes para lógica
bool isUmidadeBaixa = umidade < 42.0;
bool isNutrientePresente = temFosforo || temPotassio;
bool phAdequado = ph >= 5.9 && ph <= 7.6;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Hello, ESP32!");
  pinMode(BTN_P, INPUT_PULLUP);
  pinMode(BTN_K, INPUT_PULLUP);
  pinMode(RELE_PIN, OUTPUT);
  digitalWrite(RELE_PIN, HIGH);
  dht.begin();

  delay(1000);
  // especificar aqui os sensores pra passar pro python inserir no sqlite
}

void loop() {
  // umidade = dht.readHumidity();
  umidade = 39.9;
  // sensor de umidade possui id = 1
  Serial.printf("{\"leitura\": {\"id_sensor\": 1, \"id_plantacao\": 1, \"valor\": %.2f}}\n", umidade);
  delay(200);

  // sensor de ph possui id = 2
  phRaw = analogRead(LDR);
  ph = (phRaw / 4095.0) * 14.0; // Simula pH de 0 a 14

  // sensor de ph possui id = 3
  temFosforo = digitalRead(BTN_P);

  // sensor de ph possui id = 4
  temPotassio = digitalRead(BTN_K);
  
  // Serial.printf("{\"umidade\": %.2f, \"ph\": %.2f, \"fosforo\": %d, \"potassio\": %d}\n",
   //           umidade, ph, temFosforo, temPotassio);

  if (isUmidadeBaixa && isNutrientePresente && phAdequado) {
    digitalWrite(RELE_PIN, LOW);
  } else {
    digitalWrite(RELE_PIN, HIGH);
  }

  delay(1000); // this speeds up the simulatio

}
