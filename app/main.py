print("----------Entry point-------------")
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Welcome to CLEM Application System!"}
