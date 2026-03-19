from repositories.remover_filme_repository import remover_filme_repository


def remover_filme(id):
    filme_removido = remover_filme_repository(id)

    if filme_removido:
        return {"message": "Filme removido com sucesso"}
    else:
        return {"message": "Falha ao remover filme"}