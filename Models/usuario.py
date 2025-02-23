from odmantic import Model
from typing import Optional

class Usuario(Model):
    nome: str
    email: Optional[str] = None
    instituicao: Optional[str] = None 
    biografia: Optional[str] = None 

class UsuarioUpdate(Model):
    nome: Optional[str] = None
    email: Optional[str] = None
    instituicao: Optional[str] = None
    biografia: Optional[str] = None