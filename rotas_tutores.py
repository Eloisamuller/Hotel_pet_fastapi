from fastapi import APIRouter, HTTPException, Path
from database import executar_sql

router = APIRouter(tags=["Tutores"])

def representar_tutor(tutor):
    return {
        "id": tutor["id"],
        "nome": tutor["nome"],
        "telefone": tutor["telefone"],
        "email": tutor["email"],
    }

@router.get("/tutores")
def listartutores():
    sql = "SELECT id, nome, telefone, email FROM tutores ORDER BY id"
    tutores = executar_sql(sql)

    return {
        "dados": [representar_tutor(tutor) for tutor in tutores],
        "sintaxesql": {"sql": sql, "parametros": []},
    }

@router.get("/tutores/{tutor_id}")
def consultartutor(tutor_id: int = Path(gt=0)):
    sql = "SELECT * FROM tutores WHERE id = %s"
    parametros = (tutor_id,)
    tutores = executar_sql(sql, parametros)

    if not tutores:
        raise HTTPException(status_code=404, detail="Tutor não encontrado.")
    
    return {
        "dados": representar_tutor(tutores[0]),
        "sintaxesql": {"sql": sql, "parametros": list(parametros)},
    }