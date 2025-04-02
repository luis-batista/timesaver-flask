from models.database import get_db

class Agendamento:
    @staticmethod
    def obter_todos(filtros=None):
        db = get_db()
        cursor = db.cursor()
        
        query = '''
        SELECT a.id, a.data, a.hora, c.nome as cliente, p.descricao as procedimento, 
               a.status, co.nome as convenio, a.cliente_id, a.procedimento_id, a.observacoes
        FROM agendamentos a
        JOIN clientes c ON a.cliente_id = c.id
        JOIN procedimentos p ON a.procedimento_id = p.id
        LEFT JOIN convenios co ON c.convenio_id = co.id
        WHERE 1=1
        '''
        
        if filtros:
            if filtros.get('data'):
                query += f" AND a.data = '{filtros['data']}'"
            if filtros.get('cliente'):
                query += f" AND c.nome LIKE '%{filtros['cliente']}%'"
            if filtros.get('procedimento'):
                query += f" AND p.descricao LIKE '%{filtros['procedimento']}%'"
        
        query += " ORDER BY a.data, a.hora"
        
        cursor.execute(query)
        return cursor.fetchall()
    
    @staticmethod
    def obter_por_id(id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM agendamentos WHERE id = ?", (id,))
        return cursor.fetchone()
    
    @staticmethod
    def criar(data, hora, cliente_id, procedimento_id, observacoes=''):
        db = get_db()
        cursor = db.cursor()
        
        # Verificar disponibilidade
        cursor.execute('''
        SELECT COUNT(*) FROM agendamentos 
        WHERE data = ? AND hora = ? AND status != 'cancelado'
        ''', (data, hora))
        
        if cursor.fetchone()[0] > 0:
            return False, "Horário já está agendado!"
        
        cursor.execute('''
        INSERT INTO agendamentos (data, hora, cliente_id, procedimento_id, observacoes)
        VALUES (?, ?, ?, ?, ?)
        ''', (data, hora, cliente_id, procedimento_id, observacoes))
        db.commit()
        return True, "Agendamento criado com sucesso!"
    
    @staticmethod
    def atualizar(id, data, hora, cliente_id, procedimento_id, observacoes, status):
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
        UPDATE agendamentos
        SET data = ?, hora = ?, cliente_id = ?, procedimento_id = ?, 
            observacoes = ?, status = ?
        WHERE id = ?
        ''', (data, hora, cliente_id, procedimento_id, observacoes, status, id))
        
        db.commit()
        return True, "Agendamento atualizado com sucesso!"
    
    @staticmethod
    def excluir(id):
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("DELETE FROM agendamentos WHERE id = ?", (id,))
        db.commit()
        return True, "Agendamento excluído com sucesso!"