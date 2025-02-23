from odmantic import Model
from typing import Optional, List
from datetime import datetime
from bson import ObjectId



class Sessao(Model):
    nome: str
    data_hora: datetime
    palestrante_id: ObjectId  

class SessaoUpdate(Model):
    nome: Optional[str] = None
    data_hora: Optional[datetime] = None
    palestrante_id: Optional[ObjectId] = None   
