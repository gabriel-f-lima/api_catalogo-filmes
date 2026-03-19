from datetime import datetime
from database import get_connection

def adicionar_filme(filme):
    sql = "INSERT INTO filmes (titulo, poster_url, ano, genero) VALUES (%s, %s, %s, %s)"
    conn = get_connection()

    try:
        params = [filme["titulo"], filme["poster_url"], filme["ano"], filme["genero"]]
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return True
    except Exception as ex:
        print('Erro ao adicionar filme------', str(ex))
        return False
    finally:
        conn.close()


