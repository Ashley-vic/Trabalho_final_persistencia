from odmantic import Model
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from .sessao import Sessao



class Evento(Model):
    nome: str
    data_inicio: datetime
    data_termino: datetime
    local: str
    descricao: str
    sessoes: List[Sessao] = [] 
    participantes_ids: List[ObjectId] = []  


class EventoUpdate(Model):
    nome: Optional[str] = None
    data_inicio: Optional[datetime] = None
    data_termino: Optional[datetime] = None
    local: Optional[str] = None
    descricao: Optional[str] = None
    sessoes_ids: Optional[list[ObjectId]] = None
    participantes_ids: Optional[list[ObjectId]] = None