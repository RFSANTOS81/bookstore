from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime import date

app = FastAPI(
    title="BookStore API",
    description="API RESTful para gerenciamento de Autores e Livros",
    version="1.0.0"
)

# ==================================================
# SCHEMAS
# ==================================================

class AutorBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    nacionalidade: str
    data_nascimento: date


class AutorCreate(AutorBase):
    pass


class Autor(AutorBase):
    id: int


class LivroBase(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=200)
    ano_publicacao: int
    genero: str
    autor_id: int


class LivroCreate(LivroBase):
    pass


class Livro(LivroBase):
    id: int


# ==================================================
# "BANCO DE DADOS" EM MEMÓRIA
# ==================================================

autores = []
livros = []

autor_id_counter = 1
livro_id_counter = 1

# ==================================================
# AUTORES
# ==================================================

@app.post(
    "/autores",
    response_model=Autor,
    status_code=status.HTTP_201_CREATED
)
def criar_autor(autor: AutorCreate):
    global autor_id_counter

    novo_autor = Autor(
        id=autor_id_counter,
        **autor.model_dump()
    )

    autores.append(novo_autor)
    autor_id_counter += 1

    return novo_autor


@app.get("/autores", response_model=List[Autor])
def listar_autores():
    return autores


@app.get("/autores/{autor_id}", response_model=Autor)
def buscar_autor(autor_id: int):

    for autor in autores:
        if autor.id == autor_id:
            return autor

    raise HTTPException(
        status_code=404,
        detail="Autor não encontrado"
    )


@app.put("/autores/{autor_id}", response_model=Autor)
def atualizar_autor(
    autor_id: int,
    dados: AutorCreate
):

    for index, autor in enumerate(autores):
        if autor.id == autor_id:

            autor_atualizado = Autor(
                id=autor_id,
                **dados.model_dump()
            )

            autores[index] = autor_atualizado

            return autor_atualizado

    raise HTTPException(
        status_code=404,
        detail="Autor não encontrado"
    )


@app.delete(
    "/autores/{autor_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_autor(autor_id: int):

    for index, autor in enumerate(autores):
        if autor.id == autor_id:
            autores.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Autor não encontrado"
    )


# ==================================================
# LIVROS
# ==================================================

@app.post(
    "/livros",
    response_model=Livro,
    status_code=status.HTTP_201_CREATED
)
def criar_livro(livro: LivroCreate):

    global livro_id_counter

    autor_existe = any(
        autor.id == livro.autor_id
        for autor in autores
    )

    if not autor_existe:
        raise HTTPException(
            status_code=404,
            detail="Autor não encontrado"
        )

    novo_livro = Livro(
        id=livro_id_counter,
        **livro.model_dump()
    )

    livros.append(novo_livro)

    livro_id_counter += 1

    return novo_livro


@app.get("/livros", response_model=List[Livro])
def listar_livros():
    return livros


@app.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro(livro_id: int):

    for livro in livros:
        if livro.id == livro_id:
            return livro

    raise HTTPException(
        status_code=404,
        detail="Livro não encontrado"
    )


@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(
    livro_id: int,
    dados: LivroCreate
):

    autor_existe = any(
        autor.id == dados.autor_id
        for autor in autores
    )

    if not autor_existe:
        raise HTTPException(
            status_code=404,
            detail="Autor não encontrado"
        )

    for index, livro in enumerate(livros):
        if livro.id == livro_id:

            livro_atualizado = Livro(
                id=livro_id,
                **dados.model_dump()
            )

            livros[index] = livro_atualizado

            return livro_atualizado

    raise HTTPException(
        status_code=404,
        detail="Livro não encontrado"
    )


@app.delete(
    "/livros/{livro_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_livro(livro_id: int):

    for index, livro in enumerate(livros):
        if livro.id == livro_id:
            livros.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Livro não encontrado"
    )


@app.get("/")
def home():
    return {
        "mensagem": "BookStore API funcionando",
        "swagger": "/docs"
    }