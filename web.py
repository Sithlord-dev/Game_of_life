from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from main import GIFGenerator
from pydantic import BaseSettings

class Settings(BaseSettings):
    SERVER_HOST: str
    SERVER_PORT: int

app = FastAPI()
app.mount("/temp", StaticFiles(directory="temp"), name="temp")
settings = Settings(SERVER_HOST="127.0.0.1", SERVER_PORT=5000)


# Create a folder to store the GIFs
if not os.path.exists('temp'):
    os.makedirs('temp')

# Generate GIFs and get the name of the file back
@app.get("/generate")
async def generate_gif():
    g = GIFGenerator()
    filename = g.generateGIF(0.5, (2,2))
    return {"filename": filename+".gif", "url": f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/{filename}.gif"}

# Return app info if the root is called
@app.get("/")
async def root():
    return {"application":"Game of Life","author": "Boughalem Mohammed", "mat_nr": 2066343}
