from fastapi import FastAPI
from Routers import eventos, usuarios, sessoes


app = FastAPI()


app.include_router(eventos.router, prefix="/eventos", tags=["eventos"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(sessoes.router, prefix="/sessoes", tags=["sessoes"])



@app.on_event("startup")
async def startup():
    print("Starting the app...")
    

@app.get("/")
def read_root():
    return {"message": "Hello from tp-02-persistencia!"}