from fastapi import FastAPI, Request
from modules.user import user_router
from modules.weather import weather_router
from modules.binance import binance_router
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["User"]) 
app.include_router(binance_router, prefix="/binance", tags=["Binance"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"]) 
templates = Jinja2Templates(directory="templates") 


@app.get("/")
def read_root():
    return {"status": "success", "message": "I am working!"}

@app.get("/login-template")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})