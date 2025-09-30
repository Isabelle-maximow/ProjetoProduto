from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
# APIRouter = rota api para o front-end;
# Request = requisição HTTP;
# Form = formulario para criar e editar ;
# UploadFile = upload de fotos;
# File = função para gravar o caminho da imagem ; 
# Depends = dependencia dp banco de dados sqlite para o fastapi;

from fastapi.responses import HTMLResponse, RedirectResponse
# HTMLResponse = resposta do html GET, POST, PUT E DELETE ;
# RedirectResponse = redirecionar a pagina ao receber o metodo 'GET';

from fastapi.templating import Jinja2Templates
# Jinja2Templates = responsavel por renderizar o front-end (html, css e js)

import os, shutil
# os = função de sistemas - pegar caminhos de pasta 'imagens'
# shutil = salvar ou pegar o caminho do diretorio 'camimho da imagem'

from sqlalchemy.orm import Session
# Session = modelagem dos dados ORM 'id, nome, preco'

from database import get_db
# get_db = coletar banco 'produtos.db' para a api 

from models import Produto
# produto = manipular o models Produtos

###############################################################

router = APIRouter() # rotas api
templates = Jinja2Templates(directory="templates") # pasta front-end

# pasta para salvar imagens:
UPLOAD_DIR = "static/uploads"

# caminho para o 'os'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# PRIMEIRA ROTA:
# rota para pagina inicial listar os produtos:
@router.get ("/", response_class=HTMLResponse)
async def listar(request: Request,
                 db: Session = Depends(get_db)): # coletar o banco de dados (produtos)
    # query no banco de dados:
    produtos = db.query(Produto).all() # puxando produtos do banco
    return templates.TemplateResponse("index.html", {
        "request": request, "produtos": produtos
    })
    
    
# rota detalhe do produto 
@router.get ("/produto/{id_produto}",
             response_class=HTMLResponse)
async def detalhe (request: Request, id_produto: int,
                   db: Session = Depends(get_db)):
    #query do produto:
    produto = db.query(Produto).filter(Produto.id == id_produto).first()
    return templates.TemplateResponse("produto.html", {
        "request": request, "produto": produto
    })