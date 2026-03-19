from database import get_connection


def remover_filme_repository(id):
    conn = get_connection()
    sql = "DELETE FROM filmes WHERE id = %s;"

    try:
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        return True

    except Exception as ex:
        print("Erro ao remover filme:", str(ex))
        return False
    finally:
        conn.close()