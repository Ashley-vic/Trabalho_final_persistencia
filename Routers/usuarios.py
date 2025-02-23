from fastapi import APIRouter, HTTPException, Depends
from odmantic import AIOEngine
from bson import ObjectId
from typing import List
from pydantic import BaseModel
from Database.Database import get_engine  
from Models.usuario import Usuario, UsuarioUpdate

router = APIRouter()

@router.post("/", response_model=Usuario)
async def criar_usuario(usuario: Usuario, engine: AIOEngine = Depends(get_engine)):
    try:
        await engine.save(usuario)
        return usuario
    except Exception as e:
        print(f"Erro ao criar usuario: {e}")

@router.post("/", response_model=Usuario)
async def criar_usuario(usuario: Usuario, engine: AIOEngine = Depends(get_engine)):
    try:
        await engine.save(usuario)
        return usuario
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")

@router.get("/", response_model=List[Usuario])
async def listar_usuarios(engine: AIOEngine = Depends(get_engine)):
    try:
        usuarios = await engine.find(Usuario)
        return usuarios
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar usuários")

@router.get("/{usuario_id}", response_model=Usuario)
async def obter_usuario(usuario_id: str, engine: AIOEngine = Depends(get_engine)):
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return Usuario(id=str(usuario.id), **usuario.dict())
    except Exception as e:
        print(f"Erro ao obter usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter usuário")

@router.put("/{usuario_id}", response_model=Usuario)
async def atualizar_usuario(usuario_id: str, usuario: UsuarioUpdate, engine: AIOEngine = Depends(get_engine)):
    try:
        db_usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
        if not db_usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        update_data = usuario.dict(exclude_unset=True)  
        for key, value in update_data.items():
            setattr(db_usuario, key, value)

        await engine.save(db_usuario)
        return db_usuario
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar usuário")

@router.delete("/{usuario_id}", status_code=204)
async def deletar_usuario(usuario_id: str, engine: AIOEngine = Depends(get_engine)):
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")

        usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(usuario_id))
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        await engine.delete(usuario)  

        return {"message": "Usuário deletado com sucesso"}
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao deletar usuário")