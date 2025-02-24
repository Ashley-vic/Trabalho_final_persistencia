## Trabalho_Final_Persistencia
> Persistência de dados de um **Sistema de Gerenciamento de Eventos Acadêmicos** utilizando MongoDB e FastAPI.

## 🚀 Diagrama de Classes 
```mermaid
classDiagram
    direction LR
    class Usuario {
        +string nome
        +string email
        +string instituicao
        +string biografia
    }
    
    class Sessao {
        +string nome
        +datetime data_hora
        +ObjectId palestrante_id
    }
    
    class Evento {
        +string nome
        +datetime data_inicio
        +datetime data_termino
        +string local
        +string descricao
        +List~Sessao~ sessoes
        +List~ObjectId~ participantes_ids
    }
    
    Usuario "1" --> "*" Evento : participa
    Evento "1" --> "*" Sessao : possui
    Usuario "1" --> "*" Sessao : palestra
```

## 🚀 Instalando Gerenciador de Eventos Acadêmicos

Para baixar o reposiótio o Gerenciador de Eventos Acadêmicos, siga estas etapas:

```
git clone <link do repositório>
```

## ☕ Usando o Gerenciador de Eventos Acadêmicos

Para usar o Gerenciador de Eventos Acadêmicos, siga estas etapas:

```
pip install uvicorn

fastapi dev main.py
```
