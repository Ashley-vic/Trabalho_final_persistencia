from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from odmantic import AIOEngine
from Database.Database import get_engine
from uuid import UUID
from bson import ObjectId
import re


from Models.evento import Evento, EventoUpdate

router = APIRouter()
engine = get_engine()


@router.post("/", response_model=Evento)
async def criar_evento(evento: Evento, engine: AIOEngine = Depends(get_engine)):
    try:
        evento.data_inicio = datetime.combine(evento.data_inicio, datetime.min.time())
        evento.data_termino = datetime.combine(evento.data_termino, datetime.min.time())
        await engine.save(evento)
        return evento
    except Exception as e:
        print(f"Erro ao criar evento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar evento")

@router.get("/", response_model=list[Evento])
async def listar_eventos(engine: AIOEngine = Depends(get_engine), limit: int = 10, offset: int = 0):
    try:
        eventos = await engine.find(Evento, skip=offset, limit=limit)
        return eventos
    except Exception as e:
        print(f"Erro ao listar eventos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar eventos")


@router.get("/{evento_id}", response_model=Evento)
async def obter_evento(evento_id: str, engine: AIOEngine = Depends(get_engine)):
    try:
        if not ObjectId.is_valid(evento_id):
            raise HTTPException(status_code=400, detail="ID do evento inválido")
    
        evento = await engine.find_one(Evento, Evento.id == ObjectId(evento_id)) 

        if not evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        return evento
    except Exception as e: 
        print(f"Erro ao obter evento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter evento")



@router.put("/{evento_id}", response_model=EventoUpdate)
async def atualizar_evento(evento_id: str, evento: EventoUpdate, engine: AIOEngine = Depends(get_engine)):
    try:
        db_evento = await engine.find_one(Evento, Evento.id == ObjectId(evento_id))
        if not db_evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        update_data = evento.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_evento, key, value)
        await engine.save(db_evento)
        return db_evento
    except Exception as e:
        print(f"Erro ao atualizar evento")
        raise HTTPException(status_code=500, detail="Erro ao atualizar evento")



@router.delete("/{evento_id}")
async def deletar_evento(evento_id: str, engine: AIOEngine = Depends(get_engine)):
    try:
        evento =  await engine.find_one(Evento, Evento.id == ObjectId(evento_id))
        if not evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        await engine.delete(evento)
        return {"message": "Evento deletado com sucesso"}
    except Exception as e:
        print(f"Erro ao detelar evento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao deletar evento")


@router.post("/{evento_id}/participantes/{participante_id}", response_model=Evento)
async def adicionar_participante(evento_id: str, participante_id: str, engine: AIOEngine = Depends(get_engine)):
    try:
        if not ObjectId.is_valid(evento_id) or not ObjectId.is_valid(participante_id):
            raise HTTPException(status_code=400, detail="ID inválido")
    
        evento = await engine.find_one(Evento, Evento.id == ObjectId(evento_id))
        if not evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
    
        if ObjectId(participante_id) in evento.participantes_ids:
            raise HTTPException(status_code=400, detail="Participante já está no evento")
    
        evento.participantes_ids.append(ObjectId(participante_id))
        await engine.save(evento)
        return evento
    except Exception as e:
        print(f"Erro ao adicionar participante")
        raise HTTPException(status_code=500, detail="Erro ao adicionar participante")

@router.delete("/{evento_id}/participantes/{participante_id}", response_model=Evento)
async def remover_participante(evento_id: str, participante_id: str, engine: AIOEngine = Depends(get_engine)):
    try:
        if not ObjectId.is_valid(evento_id) or not ObjectId.is_valid(participante_id):
            raise HTTPException(status_code=400, detail="ID inválido")
    
        evento = await engine.find_one(Evento, Evento.id == ObjectId(evento_id))
        if not evento:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
    
        if ObjectId(participante_id) not in evento.participantes_ids:
            raise HTTPException(status_code=400, detail="Participante não está no evento")
    
        evento.participantes_ids.remove(ObjectId(participante_id))
        await engine.save(evento)
        return evento
    except Exception as e:
        print(f"Erro ao deletar participante do evento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao deletar participante do evento")

@router.get("/buscar/{nome}", response_model=list[Evento])
async def buscar_evento_por_nome(nome: str, engine: AIOEngine = Depends(get_engine)):
    try:
        regex = re.compile(f".*{nome}.*", re.IGNORECASE)
        eventos = await engine.find(Evento, Evento.nome.match(regex))
        if not eventos:
            raise HTTPException(status_code=404, detail="Nenhum evento encontrado com esse nome")
        return eventos
    except Exception as e:
        print(f"Erro na busca do evento pelo nome: {e}")
        raise HTTPException(status_code=500, detail="Erro na busca do evento pelo nome")

@router.get("/participante/{participante_id}/eventos", response_model=list[Evento])
async def listar_eventos_por_participante(participante_id: str, engine: AIOEngine = Depends(get_engine)):
    try:
        if not ObjectId.is_valid(participante_id):
            raise HTTPException(status_code=400, detail="ID do participante inválido")
    
        eventos = await engine.find(Evento, Evento.participantes_ids == ObjectId(participante_id))
        if not eventos:
            raise HTTPException(status_code=404, detail="Nenhum evento encontrado para este participante")
        return eventos
    except Exception as e:
        print(f"Erro ao encontrar eventos pelo participante: {e}")
        raise HTTPException(status_code=500, detail="Erro ao encontrar eventos pelo participante")


@router.get("/busca/intervalo", response_model=list[Evento])
async def buscar_eventos_por_intervalo(data_inicio: datetime, data_termino: datetime, engine: AIOEngine = Depends(get_engine)):
    try:
        if data_inicio > data_termino:
         raise HTTPException(status_code=400, detail="A data de início deve ser anterior à data de término")
    
        eventos = await engine.find(Evento, Evento.data_inicio >= data_inicio, Evento.data_termino <= data_termino)
        if not eventos:
            raise HTTPException(status_code=404, detail="Nenhum evento encontrado no intervalo de tempo especificado")
        return eventos
    except Exception as e:
        print(f"Erro ao encontrar evento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao encontrar evento")