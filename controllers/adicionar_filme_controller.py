from repositories.adicionar_filme_repository import adicionar_filme


def adiconar_filme_controller(filme):
    filme_salvo = adicionar_filme(filme)

    if filme_salvo:
        return {"message": "Filme salvo com sucesso"}
    else:
        return {"message": "Erro ao salvar filme"}