from repositories.buscar_filme_porID_repository import buscar_filme_porID


def buscar_filme_porID_controller(id):
    filme = buscar_filme_porID(id)
    if filme:
        return filme
    else:
        return {"message": "Filme não encontrado!"}