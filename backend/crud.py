from database import Database

#  Operações do tipo "C" - Create/Insert

def criar_plantacao(db: Database, nome, data_inicio, data_fim, cultura, localizacao):
    db.cursor.execute(
        "INSERT INTO plantacoes (nome, data_inicio, data_fim, cultura, localizacao) VALUES (?, ?, ?, ?, ?)",
        (nome, data_inicio, data_fim, cultura, localizacao)
        )
    db.connection.commit()

def criar_sensor(db: Database, tipo_sensor, modelo, unidade_medida):
    db.cursor.execute(
        "INSERT INTO sensores (tipo_sensor, modelo, unidade_medida) VALUES (?, ?, ?)",
        (tipo_sensor, modelo, unidade_medida)
        )
    db.connection.commit()

def inserir_leitura(db: Database, dados):
    db.cursor.execute(
        "INSERT INTO leituras_sensores (id_sensor, id_plantacao, valor, data_hora) VALUES (?, ?, ?, ?)",
        dados
    )
    db.connection.commit()

def inserir_aplicacao(db: Database, dados):
    db.cursor.execute(
        "INSERT INTO aplicacoes_agua (id_plantacao, data_inicio, data_fim,                 quantidade_litros) VALUES(?, ?, ?, ?)", dados)
    db.connection.commit()

# Operações do tipo "R" - Read/Consult

def listar_plantacoes(db: Database):
    return db.cursor.execute("SELECT * FROM plantacoes").fetchall()

def listar_leituras(db: Database):
    return db.cursor.execute('SELECT * FROM leituras_sensores').fetchall()
    
def listar_aplicacoes(db: Database):
    return db.cursor.execute('SELECT * FROM aplicacoes_agua').fetchall()

# Operações do tipo "U" - Update/Edit
def atualizar_plantacao(db: Database, id_plantacao, nome):
    db.cursor.execute(
        "UPDATE plantacoes SET nome = ? WHERE id_plantacao = ?",
        (nome, id_plantacao)
    )
    db.connection.commit()

# Operações do tipo "D" - Deletar/Remover
def deletar_plantacao(db: Database, id_plantacao):
    db.cursor.execute(
        "DELETE FROM plantacoes WHERE id_plantacao = ?",
        (id_plantacao)
    )
    db.connection.commit()