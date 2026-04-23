from datetime import datetime
from database import get_connection

def adicionar_filme(filme):
    sql = "INSERT INTO filmes (titulo, url_capa, ano, genero) VALUES (%s, %s, %s, %s)"
    conn = get_connection()
    try:
        # Garanta que a chave aqui seja a mesma que você envia do app.py
        params = [filme["titulo"], filme["url_capa"], filme["ano"], filme["genero"]]
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return True
    except Exception as ex:
        print('Erro ao adicionar filme------', str(ex))
        return False
    finally:
        conn.close()


