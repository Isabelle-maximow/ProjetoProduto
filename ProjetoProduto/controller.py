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

from database import get_db, SessionLocal
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
    
################################################

# CRUD DOS PRODUTOS

# função criar produtos:
async def criar_produto(
    nome: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    imagem: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # caminho para salvar a imagem:
    caminho = os.path.join(UPLOAD_DIR, imagem.filename) # em banco, apenas se salva o filename e NÃO IMAGEM
    with open(caminho, "wb") as arquivo:
        shutil.copyfileobj(imagem.file, arquivo) # shutil pega o caminho e arquiva/salva o arquivo
        
        # grava o produto:
        novo = Produto(nome = nome, preco = preco, quantidade = quantidade, imagem = imagem.filename)
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    
# rota da api para criar um item novo:
@router.get("/novo", response_class=HTMLResponse)
async def form_novo(request: Request):
    return templates.TemplateResponse("novo.html", {
        "request": request
    })
    
# criar metodo post para criar:
@router.post("/novo")
async def criar(
    nome: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    imagem: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    await criar_produto(nome, preco, quantidade, imagem, db)
    return RedirectResponse("/", status_code=303)

# editar produto:
async def atualizar_produto(
    id: int,
    nome: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    imagem: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # buscar produto pelo id:
    produto = db.query(Produto).filter(Produto.id == id).filter()
    if not produto:
        return None
    produto.nome = nome,
    produto.preco = preco,
    produto.quantidade = quantidade,
    if imagem and imagem.filename != "":
        # caminho para salvar:
        caminho = os.path.join(UPLOAD_DIR, imagem.filename) # em banco, apenas se salva o filename e NÃO IMAGEM
        with open(caminho, "wb") as arquivo:
            shutil.copyfileobj(imagem.file, arquivo) # shutil pega o caminho e arquiva/salva o arquivo
        produto.imagem = imagem.filename
    db.commit()
    db.refresh(produto)
    return produto

# rota para editar o produto: 
@router.get("/editar/{id}", response_class=HTMLResponse)
async def form_editar(
    id: int, request: Request, db: Session = Depends(get_db)
):
    # query produto id:
    produto = db.query(Produto).filter(Produto).first()
    return templates.TemplateResponse("editar.html", {
        "request": request, "produto": produto
    })
        
# metodo editar
@router.post("/editar/{id}")
async def editar(
    id: int,
    nome: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    imagem: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    await criar_produto(nome, preco, quantidade, imagem, db)
    return RedirectResponse("/", status_code=303)

###############################################################
# deletar produto:
async def deletar_produto(
    id: int,
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if produto:
        db.delete(produto)
        db.commit()
    else:
        return None
    return produto

# rota p deletar:
@router.get("/deletar/{id}")
async def deletar(id: int,
                  db: Session = Depends(get_db)):
    await deletar_produto(id, db)
    return RedirectResponse("/", status_code= 303)