from sqlalchemy import Column, Integer, String, Float
from database import Base, engine, SessionLocal

# tabela produtos:
class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    imagem = Column(String, nullable=True)
    
# criar banco de dados com a tabela e colunas:
Base.metadata.create_all(bind = engine)

# criar dados no banco:
'''
nome = "camisa"
preco = 89.45
quantidade = 20
imagem =  "sem foto"
novo = Produto(nome = nome, preco = preco, quantidade = quantidade,
               imagem = imagem)
db = SessionLocal()
db.add(novo)
db.commit()
'''