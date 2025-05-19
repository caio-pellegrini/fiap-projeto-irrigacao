#include "DHT.h"

// Definições de pinos
#define BTN_FOSFORO_PIN 13     // Pino botão - simula presença de Fósforo
#define BTN_POTASSIO_PIN 14    // Pino botão - simula presença de Potássio
#define LDR_PIN 34             // Pino LDR - simula leitura de pH
#define DHTPIN 23              // Pino sensor de umidade (DHT22)
#define DHTTYPE DHT22          // Tipo do sensor DHT utilizado
#define RELE_PIN 17            // Pino aciona o relé da bomba d'água
#define LED_PIN 16             // Pino LED indicador do estado da bomba

// Instancia o sensor DHT
DHT dht(DHTPIN, DHTTYPE);

// Variáveis de leitura dos sensores
float umidade, phRaw, ph;
bool temFosforo, temPotassio;

// Variáveis para controle lógico
bool isUmidadeBaixa, isNutrientePresente, phAdequado;

void setup() {
  // Inicializa a comunicação serial
  Serial.begin(115200);

  // Configura os pinos de entrada com resistor de pull-up interno
  pinMode(BTN_FOSFORO_PIN, INPUT_PULLUP);
  pinMode(BTN_POTASSIO_PIN, INPUT_PULLUP);

  // Configura os pinos de saída para relé e LED
  pinMode(RELE_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  // Garante que a bomba inicie desligada (RELE em HIGH) e o LED apagado
  digitalWrite(RELE_PIN, HIGH);
  digitalWrite(LED_PIN, LOW);

  // Inicializa o sensor DHT
  dht.begin();

  // Pequeno atraso para garantir a estabilidade dos sensores na inicialização
  delay(1000);
}

void loop() {
  // Leitura do sensor de umidade do solo
  // Envio do valor em formato JSON pela porta Serial
  // O atraso de 200ms assegura leitura correta pelo Python
  umidade = dht.readHumidity();
  Serial.printf("{\"leitura\": {\"id_sensor\": 1, \"id_plantacao\": 1, \"valor\": %.2f}}\n", umidade);
  delay(200);

  // Leitura do LDR simulando pH
  phRaw = analogRead(LDR_PIN);
  ph = (phRaw / 4095.0) * 14.0; // Conversão para escala de pH (0-14)
  Serial.printf("{\"leitura\": {\"id_sensor\": 2, \"id_plantacao\": 1, \"valor\": %.1f}}\n", ph);
  delay(200);

  // Leitura do botão simulando presença de Fósforo
  temFosforo = digitalRead(BTN_FOSFORO_PIN);
  Serial.printf("{\"leitura\": {\"id_sensor\": 3, \"id_plantacao\": 1, \"valor\": %d}}\n", temFosforo);
  delay(200);

  // Leitura do botão simulando presença de Potássio
  temPotassio = digitalRead(BTN_POTASSIO_PIN);
  Serial.printf("{\"leitura\": {\"id_sensor\": 4, \"id_plantacao\": 1, \"valor\": %d}}\n", temPotassio);
  delay(200);

  // Avaliação das condições para irrigação:
  // 1. Umidade abaixo do ideal
  // 2. Presença de pelo menos um dos nutrientes
  // 3. pH dentro da faixa adequada
  isUmidadeBaixa = umidade < 42.0;
  isNutrientePresente = temFosforo || temPotassio;
  phAdequado = ph >= 5.9 && ph <= 7.6;

  // Verifica se todas as condições estão satisfeitas para irrigação
  if (isUmidadeBaixa && isNutrientePresente && phAdequado) {
    // Ativa a bomba d'água (RELE em LOW) e acende o LED indicador
    digitalWrite(RELE_PIN, LOW);
    digitalWrite(LED_PIN, HIGH);

    // Registra o tempo de início para cálculo da duração da irrigação
    unsigned long tempo_inicio = millis();

    // Irriga por 5s (pode ser ajustado para parar ao atingir umidade ideal)
    delay(5000);

    // Calcula o tempo total de irrigação
    int tempo_aplicacao = millis() - tempo_inicio;

    // Define a quantidade de água aplicada (em litros)
    int quantidade_litros = 4;

    // Desliga a bomba (RELE em HIGH) e apaga o LED
    digitalWrite(RELE_PIN, HIGH);
    digitalWrite(LED_PIN, LOW);

    // Envio do registro de aplicação em formato JSON pela porta Serial
    Serial.printf("{\"aplicacao_agua\": {\"id_plantacao\": 1, \"tempo_aplicacao\": %d, \"quantidade_litros\": %d}}\n", tempo_aplicacao, quantidade_litros);
    delay(200);
  }
}
