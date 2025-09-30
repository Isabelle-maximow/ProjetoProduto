from fastapi import FastAPI # principal
from controller import router # backend
from fastapi.staticfiles import StaticFiles # montar pasta 'imagens'

# app da aplicação:
app = FastAPI (title="MVC Produtos")

#montar a pasta das imgs:
app.mount("/static", StaticFiles(directory="static"),
          name = "static")

# incluir a rota das apis:
app.include_router(router)

# rodar a aplicação:
# python -m uvicorn main:app --reload