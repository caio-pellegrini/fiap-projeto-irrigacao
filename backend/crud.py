from database import Database


#  Operações do tipo "C" - Create/Insert

def inserir_plantacao(db: Database, dados):
    db.cursor.execute(
        "INSERT INTO plantacoes (nome, data_inicio, data_fim, cultura, localizacao) VALUES (?, ?, ?, ?, ?)",
        dados)
    db.connection.commit()

def inserir_sensor(db: Database, dados):
    db.cursor.execute(
        "INSERT INTO sensores (tipo_sensor, modelo, unidade_medida) VALUES (?, ?, ?)",
        dados)
    db.connection.commit()

def inserir_leitura(db: Database, dados):
    db.cursor.execute(
        "INSERT INTO leituras_sensores (id_sensor, id_plantacao, valor, data_hora) VALUES (?, ?, ?, ?)",
        dados)
    db.connection.commit()

def inserir_aplicacao(db: Database, dados):
    db.cursor.execute(
        "INSERT INTO aplicacoes_agua (id_plantacao, data_inicio, data_fim, quantidade_litros) VALUES(?, ?, ?, ?)",
        dados)
    db.connection.commit()


# Operações do tipo "R" - Read/Consult

def listar_plantacoes(db: Database):
    return db.cursor.execute("SELECT * FROM plantacoes").fetchall()

def listar_leituras(db: Database):
    return db.cursor.execute('SELECT * FROM leituras_sensores').fetchall()
    
def listar_aplicacoes(db: Database):
    return db.cursor.execute('SELECT * FROM aplicacoes_agua').fetchall()

def listar_leituras_periodo(db: Database, data_inicio, data_fim):
    return db.cursor.execute('SELECT * FROM leituras_sensores WHERE data_hora BETWEEN ? AND ?', (data_inicio, data_fim)).fetchall()


# Operações do tipo "U" - Update/Edit

def atualizar_plantacao(db: Database, id_plantacao, dados):
    """
    Atualiza os dados de uma plantação com base no ID.

    Parâmetros:
    - id_plantacao (int): ID da plantação a ser atualizada
    - dados (tuple): Nova tupla contendo (nome, data_inicio, data_fim, cultura, localizacao)
    """
    db.cursor.execute("""
        UPDATE plantacoes
        SET nome = ?, data_inicio = ?, data_fim = ?, cultura = ?, localizacao = ?
        WHERE id_plantacao = ?
    """, (*dados, id_plantacao))
    db.connection.commit()

def atualizar_sensor(db: Database, id_sensor, dados):
    """
    Atualiza os dados de um sensor com base no ID.
    
    Parâmetros:
    - id_sensor (int): ID do sensor a ser atualizado
    - dados (tuple): Nova tupla contendo (tipo_sensor, modelo, unidade_medida)
    """
    db.cursor.execute("""
        UPDATE sensores
        SET tipo_sensor = ?, modelo = ?, unidade_medida = ?
        WHERE id_sensor = ?
    """, (*dados, id_sensor))
    db.connection.commit()


# Operações do tipo "D" - Deletar/Remover
def deletar_plantacao(db: Database, id_plantacao):
    db.cursor.execute(
        "DELETE FROM plantacoes WHERE id_plantacao = ?",
        id_plantacao
    )
    db.connection.commit()

def deletar_sensor(db: Database, id_sensor):
    db.cursor.execute(
        "DELETE FROM sensores WHERE id_sensor = ?",
        id_sensor
    )
    db.connection.commit()

def deletar_leitura(db: Database, id_leitura):
    db.cursor.execute(
        "DELETE FROM leituras_sensores WHERE id_leitura = ?",
        (id_leitura,)
    )
    db.connection.commit()