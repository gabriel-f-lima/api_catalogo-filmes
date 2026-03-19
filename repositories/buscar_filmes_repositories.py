
from psycopg2.extras import RealDictCursor

from database import get_connection

def buscar_todos_filmes_repositories():

    sql = "SELECT * FROM filmes;"
    conn = get_connection()

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql)
        filmes = cursor.fetchall()
        print('filmes---------', filmes)

        return filmes
    except Exception as ex:
        print('Erro ao buscar filmes', str(ex))
        return []

    finally:
        conn.close()
