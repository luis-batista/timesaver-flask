import sqlite3

DB_NAME = "clinica.db"

def conectar():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            convenio_id INTEGER,
            FOREIGN KEY (convenio_id) REFERENCES convenios(id)
        );

        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            crm TEXT UNIQUE NOT NULL,
            especialidade TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS convenios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            codigo_ans TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS procedimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_tuss TEXT UNIQUE NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            paciente_id INTEGER NOT NULL,
            medico_id INTEGER NOT NULL,
            procedimento_id INTEGER NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
            FOREIGN KEY (medico_id) REFERENCES medicos(id),
            FOREIGN KEY (procedimento_id) REFERENCES procedimentos(id)
        );
    """)

    conn.commit()
    conn.close()
