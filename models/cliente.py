from models.database import get_db

class Cliente:
    @staticmethod
    def obter_todos():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
        SELECT c.id, c.nome, c.telefone, c.email, co.nome as convenio, c.num_carteirinha, c.convenio_id
        FROM clientes c
        LEFT JOIN convenios co ON c.convenio_id = co.id
        ''')
        
        return cursor.fetchall()
    
    @staticmethod
    def obter_por_id(id):
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
        SELECT c.id, c.nome, c.telefone, c.email, c.convenio_id, c.num_carteirinha
        FROM clientes c
        WHERE c.id = ?
        ''', (id,))
        
        return cursor.fetchone()
    
    @staticmethod
    def obter_para_select():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, nome FROM clientes")
        return cursor.fetchall()
    
    @staticmethod
    def criar(nome, telefone, email='', convenio_id=1, num_carteirinha=''):
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
        INSERT INTO clientes (nome, telefone, email, convenio_id, num_carteirinha)
        VALUES (?, ?, ?, ?, ?)
        ''', (nome, telefone, email, convenio_id, num_carteirinha))
        
        db.commit()
        return True, "Cliente cadastrado com sucesso!"
        
    @staticmethod
    def atualizar(id, nome, telefone, email='', convenio_id=1, num_carteirinha=''):
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
        UPDATE clientes
        SET nome = ?, telefone = ?, email = ?, convenio_id = ?, num_carteirinha = ?
        WHERE id = ?
        ''', (nome, telefone, email, convenio_id, num_carteirinha, id))
        
        db.commit()
        return True, "Cliente atualizado com sucesso!"
        
    @staticmethod
    def excluir(id):
        db = get_db()
        cursor = db.cursor()
        
        # Verificar se há agendamentos para este cliente
        cursor.execute("SELECT COUNT(*) FROM agendamentos WHERE cliente_id = ?", (id,))
        if cursor.fetchone()[0] > 0:
            return False, "Não é possível excluir cliente com agendamentos!"
        
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
        db.commit()
        return True, "Cliente excluído com sucesso!"