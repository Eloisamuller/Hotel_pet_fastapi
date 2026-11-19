import logging

from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError

from database import executar_sql

app = FastAPI(title="API de Hotel Pet — Desenvolvimento Web II")


@app.exception_handler(MySQLError)
def erro_de_banco(request: Request, exc: MySQLError):
    logging.getLogger("uvicorn.error").error("Erro no MySQL: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Não foi possível acessar o banco de dados."},
    )


@app.get("/")
def raiz():
    return {"mensagem": "API do Hotel Pet rodando com sucesso! Acesse /docs para ver a documentação."}


def representar_tutor(tutor):
    return {
        "id": tutor["id"],
        "nome": tutor["nome"],
        "telefone": tutor["telefone"],
        "email": tutor["email"],
    }


def representar_pet(pet):
    return {
        "id": pet["id"],
        "nome": pet["nome"],
        "especie": pet["especie"],
        "raca": pet["raca"],
        "tutor_id": pet["tutor_id"],
    }


@app.get("/tutores")
def listartutores():
    sql = "SELECT id, nome, telefone, email FROM tutores ORDER BY id"
    tutores = executar_sql(sql)

    return {
        "dados": [representar_tutor(tutor) for tutor in tutores],
        "sintaxesql": {"sql": sql, "parametros": []},
    }


@app.get("/tutores/{tutor_id}")
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


@app.get("/pets")
def listarpets(
    especie: str | None = Query(default=None, min_length=1, max_length=50)
):
    sql = "SELECT id, nome, especie, raca, tutor_id FROM pets"
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


@app.get("/pets/{pet_id}")
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

@app.get("/teste-conexao")
def testar_conexao():
    resultado = executar_sql("SELECT DATABASE() as banco, COUNT(*) as total_tutores FROM tutores")
    return {"status": "Conectado com sucesso!", "detalhes": resultado}