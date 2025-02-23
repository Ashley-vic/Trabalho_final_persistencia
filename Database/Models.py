from odmantic import Model
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class Usuario(Model):
    nome: str
    email: Optional[str] = None
    instituicao: Optional[str] = None 
    biografia: Optional[str] = None 

class Sessao(Model):
    nome: str
    data_hora: datetime
    palestrante_id: ObjectId  

class Evento(Model):
    nome: str
    data_inicio: datetime
    data_termino: datetime
    local: str
    descricao: str
    sessoes: List[Sessao] = [] 
    participantes_ids: List[ObjectId] = []  
