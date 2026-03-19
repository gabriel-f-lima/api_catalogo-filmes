from datetime import datetime
from repositories.buscar_filmes_repositories import buscar_todos_filmes_repositories


def buscar_filmes_controller():
    filmes = buscar_todos_filmes_repositories()
    for filme in filmes:
        if filme.get("ano"):
            try:
                if isinstance(filme["ano"], str):
                    data_obj = datetime.strptime(filme["ano"], "%Y-%m-%d")
                    filme["ano"] = data_obj.strftime("%d/%m/%Y")
                elif isinstance(filme["ano"], datetime):
                    filme["ano"] = filme["ano"].strftime("%d/%m/%Y")
            except Exception:
                pass
    return filmes
