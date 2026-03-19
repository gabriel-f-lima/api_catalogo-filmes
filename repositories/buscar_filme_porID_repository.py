from psycopg2.extras import RealDictCursor
from database import get_connection


def buscar_filme_porID(id):
    sql = "SELECT * FROM filmes WHERE id = %s"
    conn = get_connection()

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        params = [id]
        cursor.execute(sql, params)
        filme = cursor.fetchone()

        return filme



    except Exception as ex:
        print('Erro ao buscar filme', str(ex))
        return []
    finally:
        conn.close()