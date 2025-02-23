from fastapi import APIRouter, HTTPException, Depends
from odmantic import AIOEngine
from Database.Database import get_engine
from bson import ObjectId
from datetime import datetime
from Models.sessao import Sessao, SessaoUpdate
from Models.evento import Evento

router = APIRouter()
engine = get_engine()

@router.post("/{evento_id}", response_model=Sessao)
async def criar_sessao(evento_id: str, sessao: Sessao, engine: AIOEngine = Depends(get_engine)):
    if not ObjectId.is_valid(evento_id):
        raise HTTPException(status_code=400, detail="ID do evento inválido")
    
    evento = await engine.find_one(Evento, Evento.id == ObjectId(evento_id))
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    
    try:
        await engine.save(sessao)
        evento.sessoes.append(sessao)
        await engine.save(evento)
        return sessao
    except Exception as e:
        print(f"Erro ao criar sessão: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar sessão")

# Listar sessões
@router.get("/", response_model=list[Sessao])
async def listar_sessoes(engine: AIOEngine = Depends(get_engine), limit: int = 10, offset: int = 0):
    sessoes = await engine.find(Sessao, skip=offset, limit=limit)
    return sessoes

# Obter sessão por ID
@router.get("/{sessao_id}", response_model=Sessao)
async def obter_sessao(sessao_id: str, engine: AIOEngine = Depends(get_engine)):
    if not ObjectId.is_valid(sessao_id):
        raise HTTPException(status_code=400, detail="ID da sessão inválido")
    
    sessao = await engine.find_one(Sessao, Sessao.id == ObjectId(sessao_id))

    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    return sessao

@router.put("/{sessao_id}", response_model=Sessao)
async def atualizar_sessao(sessao_id: str, sessao: SessaoUpdate, engine: AIOEngine = Depends(get_engine)):
    db_sessao = await engine.find_one(Sessao, Sessao.id == ObjectId(sessao_id))
    if not db_sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    update_data = sessao.dict(exclude_unset=True)  
    for key, value in update_data.items():
        setattr(db_sessao, key, value)

    await engine.save(db_sessao)
    return db_sessao


# Deletar sessão
@router.delete("/{sessao_id}")
async def deletar_sessao(sessao_id: str, engine: AIOEngine = Depends(get_engine)):
    if not ObjectId.is_valid(sessao_id):
        raise HTTPException(status_code=400, detail="ID da sessão inválido")
    
    sessao = await engine.find_one(Sessao, Sessao.id == ObjectId(sessao_id))
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    await engine.delete(sessao)
    return {"message": "Sessão deletada com sucesso"}



@router.get("/palestrante/eventos/{palestrante_id}", response_model=list[Evento])
async def obter_eventos_por_palestrante(palestrante_id: str, engine: AIOEngine = Depends(get_engine)):
    if not ObjectId.is_valid(palestrante_id):
        raise HTTPException(status_code=400, detail="ID do palestrante inválido")
    
    palestrante_id = ObjectId(palestrante_id)

    eventos = await engine.find(Evento, {"sessoes.palestrante_id": palestrante_id})

    if not eventos:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado para este palestrante")

    return eventos