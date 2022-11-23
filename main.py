from fastapi import FastAPI
from models import Pessoa,Tokens,session
from secrets import token_hex
import datetime

app = FastAPI()

@app.post('/cadastro')
def cadastro(nome: str, senha: str, user: str ):
    usuarios = session.query(Pessoa).filter_by(usuario=user).all()
    if len(usuarios) > 0:
        return{'Mensagem':"Usuario já cadastrado"}
    elif len(senha) < 8:
        return{'Mensagem':"Senha muito fraca.Digite uma senha com no minimo 8 digitos"}
    else:
        adicionar_pessoa = Pessoa(nome=nome, senha=senha,usuario=user)
        session.add(adicionar_pessoa)
        session.commit()
        return{'Mensagem':"Cadastro com Sucesso"}
    
@app.post('/login')
def login(user: str, senha: str):
    usuario_login = session.query(Pessoa).filter_by(usuario=user, senha=senha).all()
    if len(usuario_login) == 0:
        return {'Mensagem':"Usuario não existe ou senha inválida"}
    
    while True:
        token = token_hex(50)
        token_existe = session.query(Tokens).filter_by(token=token).all()
        if len(token_existe) == 0:
            pessoa_existe = session.query(Tokens).filter_by(id_pessoa=usuario_login[0].id).all()
            if len(pessoa_existe) == 0:
                novo_token = Tokens(id_pessoa=usuario_login[0].id, token=token)
                session.add(novo_token)
            elif len(pessoa_existe) > 0:
                pessoa_existe[0].token = token
                pessoa_existe[0].data = datetime.datetime.utcnow()
            
            session.commit()
            break
    return token




    