import sqlite3

class Database:
    def __init__(self, db_name='farmtech.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
    
    def criar_database(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS plantacoes (
                id_plantacao INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100),
                data_inicio DATETIME,
                data_fim DATETIME,
                cultura VARCHAR(50),
                localizacao VARCHAR(200)
            );

            CREATE TABLE IF NOT EXISTS sensores (
                id_sensor INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_sensor VARCHAR(50),
                modelo VARCHAR(50),
                unidade_medida VARCHAR(10)
            );

            CREATE TABLE IF NOT EXISTS leituras_sensores (
                id_leitura INTEGER PRIMARY KEY AUTOINCREMENT,
                id_sensor INTEGER,
                id_plantacao INTEGER,
                valor FLOAT,
                data_hora DATETIME,
                FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor),
                FOREIGN KEY (id_plantacao) REFERENCES plantacoes(id_plantacao)
            );

            CREATE TABLE IF NOT EXISTS aplicacoes_agua (
                id_aplicacao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_plantacao INTEGER,
                data_inicio DATETIME,
                data_fim DATETIME,
                quantidade_litros INTEGER,
                FOREIGN KEY (id_plantacao) REFERENCES plantacoes(id_plantacao)
            )
        """)
        self.connection.commit()

    def preencher_database(self):
        self.cursor.executescript("""
            INSERT INTO plantacoes (nome, data_inicio, data_fim, cultura, localizacao)
            VALUES ('Plantação Teste', '2025-05-01', '2025-05-30', 'Milho', 'Monte Alto - SP');
            
            INSERT INTO sensores (tipo_sensor, modelo, unidade_medida)
            VALUES
                ('umidade', 'dht22', '%'),
                ('ph', 'ldr', 'ph'),
                ('fosforo', 'pushbutton', 'presenca'),
                ('potassio', 'pushbutton', 'presenca');
        """)
        self.connection.commit()

    def limpar_database(self):
        self.cursor.executescript("""
            DROP TABLE IF EXISTS plantacoes;
            DROP TABLE IF EXISTS sensores;
            DROP TABLE IF EXISTS leituras_sensores;
            DROP TABLE IF EXISTS aplicacoes_agua; 
        """)
        self.connection.commit()

    def close(self):
        self.connection.close()

    def inserir_leitura(self, dados):
        self.cursor.execute("INSERT INTO leituras_sensores (id_sensor, id_plantacao, valor, data_hora) VALUES()", dados)



    