import uvicorn
import nest_asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from utils import call2InsightRest

app = FastAPI(title='Deploying with FastAPI')


# By using @app.get("/") you are allowing the GET method to work for the / endpoint.

@app.get("/")
def home():
    return "Congratulations! Your API is working as expected. Author: Tung Khong Manh. Now head over to " \
           "http://localhost:8000/docs. "


@app.post("/predict")
async def prediction(idUser: int, isReset: int = 0, fileUpload: UploadFile = File(...)):
    # 1. VALIDATE INPUT FILE
    filename = fileUpload.filename
    fileExtension = filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not fileExtension:
        raise HTTPException(status_code=415, detail="Unsupported file provided.")
    if not isinstance(idUser, int):
        raise HTTPException(status_code=415, detail="id user must be int")

    # call server of insightFace REST
    server = 'http://localhost:18081/extract'
    res = call2InsightRest(file=fileUpload, user_id=idUser, server=server, isReset=isReset)
    if (isinstance(res, str)):
        # Return add sucess
        return res
    else:
        # Return score Emd of Eul and Cos
        return {'mindistEuc': res[0], 'mindistCos': res[1], "result": min(res)}


# Allows the server to be run in this interactive environment
nest_asyncio.apply()

# Host depends on the setup you selected (docker or virtual env)
host = "0.0.0.0" if os.getenv("DOCKER-SETUP") else "127.0.0.1"

# Spin up the server!
uvicorn.run(app, host=host, port=8000)
