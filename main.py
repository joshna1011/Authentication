from fastapi import FastAPI
from modules.user import user_router

app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["User"])  

@app.get("/")
def read_root():
    return {"Hello": "World"}