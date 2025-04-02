import sqlite3
import os
from flask import current_app, g

def get_db():
    if 'db' not in g:
        os.makedirs(os.path.dirname(current_app.config['DATABASE_PATH']), exist_ok=True)
        g.db = sqlite3.connect(current_app.config['DATABASE_PATH'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()
    
    # Tabela de convênios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS convenios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        codigo TEXT NOT NULL
    )
    ''')
    
    # Tabela de procedimentos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS procedimentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_tuss TEXT NOT NULL,
        descricao TEXT NOT NULL,
        duracao_minutos INTEGER NOT NULL
    )
    ''')
    
    # Tabela de clientes/pacientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT,
        convenio_id INTEGER,
        num_carteirinha TEXT,
        FOREIGN KEY (convenio_id) REFERENCES convenios (id)
    )
    ''')
    
    # Tabela de agendamentos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        hora TEXT NOT NULL,
        cliente_id INTEGER NOT NULL,
        procedimento_id INTEGER NOT NULL,
        observacoes TEXT,
        status TEXT DEFAULT 'agendado',
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (procedimento_id) REFERENCES procedimentos (id)
    )
    ''')
    
    # Inserir alguns dados de exemplo
    # Convênios
    cursor.execute("INSERT OR IGNORE INTO convenios (id, nome, codigo) VALUES (1, 'Particular', '00')")
    cursor.execute("INSERT OR IGNORE INTO convenios (id, nome, codigo) VALUES (2, 'Unimed', '01')")
    cursor.execute("INSERT OR IGNORE INTO convenios (id, nome, codigo) VALUES (3, 'Amil', '02')")
    
    # Procedimentos TUSS
    cursor.execute("INSERT OR IGNORE INTO procedimentos (id, codigo_tuss, descricao, duracao_minutos) VALUES (1, '10101012', 'Consulta Clínica', 30)")
    cursor.execute("INSERT OR IGNORE INTO procedimentos (id, codigo_tuss, descricao, duracao_minutos) VALUES (2, '10101039', 'Avaliação Inicial', 45)")
    cursor.execute("INSERT OR IGNORE INTO procedimentos (id, codigo_tuss, descricao, duracao_minutos) VALUES (3, '20101236', 'Exame de Rotina', 20)")
    
    db.commit()