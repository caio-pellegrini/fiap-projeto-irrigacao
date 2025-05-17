import serial
import json
from datetime import datetime
import database

# Conecta à porta COM (veja no Gerenciador de Dispositivos)
espSerial = serial.Serial('COM4', 115200)

db = database.Database()

print('Configurando database...')

# Limpar banco de dados (excluir dados para nova simulação)
db.limpar_database()
# Criar banco de dados de acordo com estrutura 'mer.puml'
db.criar_database()
# Preenche com plantação teste e 4 sensores do desafio
db.preencher_database()

print("Lendo dados do ESP32...")

id_plantacao = 1 # apenas um teste, temos uma plantação só

while True:
    try:
        data = espSerial.readline().decode('utf-8').strip()
        # print(f"Recebido: {data}")
        leitura = json.loads(data)['leitura']
        # print(f"Leitura: {leitura}")
        timestamp = datetime.now().isoformat()

        db.inserir_leitura((leitura['id_sensor'], id_plantacao, leitura['valor'], timestamp))

    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Erro ao decodificar: {e}")
    except KeyboardInterrupt:
        print("Programa encerrado")
        break

espSerial.close()
db.close()









