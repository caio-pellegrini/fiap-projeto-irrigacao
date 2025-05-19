import serial
import json
from datetime import datetime, timedelta
from database import Database
from crud import *

db = Database()

print('Configurando database...')

# Limpar banco de dados (excluir dados para nova simulação)
db.excluir_tabelas()
# Criar banco de dados e tabelas de acordo com estrutura 'mer.puml'
db.criar_tabelas()

# Preenche com plantação teste e 4 sensores do desafio
inserir_plantacao(db, ('Plantação Teste', '2025-05-01', '2025-05-30', 'Milho', 'Monte Alto - SP'))
inserir_sensor(db, ('umidade', 'dht22', '%'))
inserir_sensor(db, ('ph', 'LDR_PIN', 'ph'))
inserir_sensor(db, ('fosforo', 'pushbutton', 'presenca'))
inserir_sensor(db, ('potassio', 'pushbutton', 'presenca'))

# Conecta à porta COM (veja no Gerenciador de Dispositivos)
espSerial = serial.Serial('COM4', 115200)

print("Lendo dados do ESP32...")

try:
    while True:
        # 1. Leitura e decodificação da linha serial
        try:
            linha = espSerial.readline().decode('utf-8').strip()
        except UnicodeDecodeError as e:
            print(f"[Erro] Falha ao decodificar linha: {e}")
            continue
        
        # 2. Parse do JSON e salvar como dicionário
        try:
            dados = json.loads(linha)
        except json.JSONDecodeError as e:
            print(f"[Erro] JSON inválido: {linha} -> {e}")
            continue

        # 3. Obter timestamp e chave principal
        timestamp = datetime.now()
        chave_raiz = list(dados.keys())[0]

        try:
            # 4. Processamento da leitura
            if chave_raiz == 'leitura':
                print('.', end=" ", flush=True)
                leitura = dados['leitura']
                data_hora = timestamp.isoformat()
                dados_para_inserir = (
                    leitura['id_sensor'],
                    leitura['id_plantacao'],
                    leitura['valor'],
                    data_hora
                )
                inserir_leitura(db, dados_para_inserir)

            # 5. Processamento da aplicação de água
            elif chave_raiz == 'aplicacao_agua':
                print("aplicacao")
                aplicacao = dados['aplicacao_agua']
                data_fim = timestamp.isoformat()
                tempo_aplicacao = timedelta(milliseconds=aplicacao['tempo_aplicacao'])
                data_inicio = timestamp - tempo_aplicacao
                dados_para_inserir = (
                    aplicacao['id_plantacao'],
                    data_inicio,
                    data_fim,
                    aplicacao['quantidade_litros']
                )
                inserir_aplicacao(db, dados_para_inserir)

            else:
                print(f"[Aviso] Tipo de dado desconhecido: {chave_raiz}")

        except KeyError as e:
            print(f"[Erro] Dado esperado não encontrado: {e}")
        except Exception as e:
            print(f"[Erro] Falha ao processar dados: {e}")

except KeyboardInterrupt:
    print("\n[Info] Execução interrompida manualmente.")

finally:
    atualizar_plantacao(db, 1, (
        "Plantação Atualizada",
        "2025-05-01",
        "2025-06-01",
        "Soja",
        "Monte Alto - SP"
    ))
    print("=============== PLANTACOES ============")
    for row in listar_plantacoes(db):
        print(row)
    print("=============== LEITURAS DOS SENSORES ============")
    deletar_leitura(db, 5)
    for row in listar_leituras(db):
        print(row)
    print("=============== APLICACOES DE ÁGUA ============")
    for row in listar_aplicacoes(db):
        print(row)

    print("Encerrando conexões...")
    espSerial.close()
    db.close()
    print("Programa encerrado!")









