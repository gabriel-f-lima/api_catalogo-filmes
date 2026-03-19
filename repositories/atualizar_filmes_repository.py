from database import get_connection

def atualizar_filmes_repository(dados, id):
    conn = get_connection()
    sql = """
          UPDATE filmes
          SET titulo = %s, \
              poster_url = %s, \
              ano    = %s, \
              genero = %s
          WHERE id = %s; \
          """

    try:
        cursor = conn.cursor()
        params = (dados["titulo"], dados["poster_url"], dados["ano"].strftime("%d/%m/%Y"), dados["genero"], id)
        cursor.execute(sql, params)
        conn.commit()
        return True
    except Exception as ex:
        print("Erro ao atualizar filme:", str(ex))
        return False
    finally:
        conn.close()