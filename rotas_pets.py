from fastapi import APIRouter, HTTPException, Path, Query
from database import executar_sql

router = APIRouter(tags=["Pets"])

def representar_pet(pet):
    return {
        "id": pet["id"],
        "nome": pet["nome"],
        "especie": pet["especie"],
        "raca": pet["raca"],
        "porte": pet["porte"],
        "tutor_id": pet["tutor_id"],
    }

@router.get("/pets")
def listarpets(
    especie: str | None = Query(default=None, min_length=1, max_length=50)
):
    sql = "SELECT id, nome, especie, raca, porte, tutor_id FROM pets"
    parametros = ()

    if especie is not None:
        sql += " WHERE especie = %s"
        parametros = (especie,)

    sql += " ORDER BY id"
    pets = executar_sql(sql, parametros)

    return {
        "dados": [representar_pet(pet) for pet in pets],
        "sintaxesql": {"sql": sql, "parametros": list(parametros)},
    }

@router.get("/pets/{pet_id}")
def consultarpet(pet_id: int = Path(gt=0)):
    sql = "SELECT * FROM pets WHERE id = %s"
    parametros = (pet_id,)
    pets = executar_sql(sql, parametros)

    if not pets:
        raise HTTPException(status_code=404, detail="Pet não encontrado.")
    
    return {
        "dados": representar_pet(pets[0]),
        "sintaxesql": {"sql": sql, "parametros": list(parametros)},
    }