from fastapi import FastAPI
from skyfield.api import Topos, load

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "yoooooo!"}

@app.get("/planets/{planet_name}")
def get_planet(planet_name:str):
    return{"planet": planet_name,"data": "Description of the planet", "location":"location of the planet"}