from repositories.atualizar_filmes_repository import atualizar_filmes_repository


def atualizar_filme(dados, id):
    filme_atualizado = atualizar_filmes_repository(dados, id)

    if filme_atualizado:
        return {"message": "Filme salvo com sucesso"}
    else:
        return {"message": "Erro ao salvar filme"}