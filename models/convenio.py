from models.database import get_db

class Convenio:
    @staticmethod
    def obter_todos():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, nome, codigo FROM convenios")
        return cursor.fetchall()