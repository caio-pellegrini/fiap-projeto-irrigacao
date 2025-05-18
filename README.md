# Sistema de Irrigação Inteligente – FarmTech Solutions

## Descrição do Projeto
Este projeto simula um sistema de irrigação inteligente para agricultura de precisão, utilizando sensores físicos integrados a um microcontrolador ESP32. O objetivo é coletar dados de sensores de umidade, nutrientes e pH do solo, controlar automaticamente uma bomba de irrigação e armazenar os dados em um banco de dados SQL para análise posterior.

---

## 1. Circuito e Componentes

O circuito foi desenvolvido e simulado na plataforma Wokwi, utilizando os seguintes componentes:

- ESP32: Microcontrolador responsável pela leitura dos sensores e controle do relé.
- Sensor de Umidade (DHT22): Mede a umidade do solo.
- Sensor de pH (LDR): Simula variações de pH através da luminosidade.
- Sensor de Fósforo (Botão): Simula presença/ausência de fósforo (pressionado = presença).
- Sensor de Potássio (Botão): Simula presença/ausência de potássio (pressionado = presença).
- Relé: Controla a bomba de irrigação.
- LED: Indica o status da bomba (ligado = irrigação ativa).

### Imagem do Circuito

![Circuito Wokwi](docs/circuito_wokwi.png)


## 2. Lógica de Controle de Irrigação

A bomba de irrigação é ativada somente quando **três condições** são simultaneamente atendidas:

1. **Umidade do solo abaixo do limite definido**  
   - Isso indica que o solo está seco e necessita de água.

2. **Pelo menos um dos nutrientes (fósforo ou potássio) está presente**  
   - Nutrientes são essenciais para o crescimento das plantas. Se ambos estiverem ausentes, a irrigação não será eficaz, pois a planta não conseguirá absorver o que precisa para se desenvolver, mesmo com água.

3. **O pH do solo está dentro da faixa adequada**  
   - O pH influencia diretamente na capacidade da planta de absorver nutrientes. Se estiver fora da faixa ideal (muito ácido ou muito básico), a irrigação pode piorar o desequilíbrio e prejudicar ainda mais o solo.

Caso **qualquer uma dessas condições não seja atendida**, a bomba é desativada automaticamente.

O status da bomba é indicado por um LED.

Trecho comentado do código:

3. Banco de Dados SQL e Operações CRUD

Os dados coletados pelo ESP32 são enviados via monitor serial e armazenados em um banco de dados SQLite utilizando Python.

Estrutura do Banco de Dados
Tabela plantacoes: Cadastro das plantações monitoradas.
Tabela sensores: Cadastro dos sensores instalados.
Tabela leituras: Armazena as leituras dos sensores (umidade, pH, fósforo, potássio, data/hora).

Relação com o MER
O modelo relacional segue o MER da Fase 2, onde:


Operações CRUD
O script Python implementa as operações básicas:

Create: Inserção de novas plantações, sensores e leituras.
Read: Consulta de leituras por plantação, sensor ou período.
Update: Atualização de dados de plantações ou sensores.
Delete: Remoção de sensores, plantações ou leituras.
Exemplos de Uso
Exemplo de Dados
id	sensor_id	umidade	ph	fosforo	potassio	data_hora
1	1	45	6.5	1	0	2024-06-01 10:00:00
2	1	42	6.7	1	1	2024-06-01 11:00:00
4. Como Executar
ESP32 (Wokwi/PlatformIO)
Abra o projeto no VS Code.
Compile e faça upload do código para o ESP32.
Visualize os dados no monitor serial.
Python (Banco de Dados)
Copie os dados do monitor serial.
Execute o script Python em backend para inserir e manipular os dados no banco SQLite.
5. Organização do Repositório
esp32: Código-fonte do ESP32.
backend: Scripts Python para banco de dados.
docs: Imagens e documentação.
README.md: Este arquivo.
6. Demonstração
[Opcional] Assista ao vídeo de demonstração:
Link para o vídeo

7. Créditos
Projeto desenvolvido para a disciplina de IoT – FIAP.

Dúvidas ou sugestões? Abra uma issue!