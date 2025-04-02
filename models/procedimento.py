from models.database import get_db

class Procedimento:
    @staticmethod
    def obter_todos():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, codigo_tuss, descricao, duracao_minutos FROM procedimentos")
        return cursor.fetchall()
    
    @staticmethod
    def obter_para_select():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, descricao FROM procedimentos")
        return cursor.fetchall()