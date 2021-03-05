from fastapi import FastAPI
import os
from main import GIFGenerator

app = FastAPI()

# Create a folder to store the GIFs
if not os.path.exists('temp'):
    os.makedirs('temp')

# Generate GIFs and get the name of the file back
@app.get("/generate")
async def generate_gif():
    g = GIFGenerator()
    return {"filename": g.generateGIF()}

# Serve the gifs in the folder
@app.get("/gif/<string:filename>")
async def get_gif(filename):
    file = open("temp/"+filename+".gif", "r+b").read()
    # Comment this if you'd actually like to save all the GIFs
    os.remove("temp/"+filename+".gif")
    return file

# Return app info if the root is called
@app.get("/")
async def root():
    return {"application":"Game of Life","author": "Boughalem Mohammed", "mat_nr": 2066343}
