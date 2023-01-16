import os
import base64
import pathlib
import shutil
from fastapi import FastAPI, Depends, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from utils.color_content import exact_color
from utils.edge_detection import edges
from utils.image_colorfulness import image_colorfulness

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = pathlib.Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "images"
COLOR_CONTENT_DIR = IMAGE_DIR / "color-content"
EDGE_DIR = IMAGE_DIR / "edge"
COLORFULNESS_DIR = IMAGE_DIR / "image-colorfulness"

folder = [IMAGE_DIR, COLOR_CONTENT_DIR, EDGE_DIR, COLORFULNESS_DIR]

@app.on_event("startup")
def on_startup():
    for i in folder:
        CHECK_FOLDER = os.path.isdir(i)
        if not CHECK_FOLDER:
            os.makedirs(i)

@app.get("/")
async def root():
    return {"message": "Welcome to my API, I wrote it out of love for you"}


@app.post("/color-content-file/")
async def color_content_file_fn(file:  UploadFile = File(description="A file read as UploadFile")):
    
    if file.content_type != f"image/{'jpeg' or 'jpg' or 'png'}":
        raise HTTPException(400, detail="Invalid file type")
    
    with open(f"{COLOR_CONTENT_DIR}/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    res = exact_color(f"{COLOR_CONTENT_DIR}/{file.filename}", 300, 12, 2.5)
    clr_cnt = {}
    for i in res:
        k,v = i.split()
        clr_cnt[k] = v
    
    response = FileResponse(f"{COLOR_CONTENT_DIR}/{file.filename}", headers=clr_cnt)
    response.set_cookie(key='color_content', value=clr_cnt, httponly=True)
    return response

@app.post("/color-content-json/")
async def color_content_json_fn(file:  UploadFile = File(description="A file read as UploadFile")):
    
    if file.content_type != f"image/{'jpeg' or 'jpg' or 'png'}":
        raise HTTPException(400, detail="Invalid file type")
    
    with open(f"{COLOR_CONTENT_DIR}/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    with open(f"{COLOR_CONTENT_DIR}/{file.filename}", "rb") as image_file:
        encoded_image_string = base64.b64encode(image_file.read())
    
    res = exact_color(f"{COLOR_CONTENT_DIR}/{file.filename}", 300, 12, 2.5)
    clr_cnt = {}
    for i in res:
        k,v = i.split()
        clr_cnt[k] = v
    
    payload = {"color_content":clr_cnt, "mime":f"image/{file.filename.split('.')[1]}", "encoded_image":encoded_image_string}
    return payload


@app.post("/edge-json/")
async def edge_feature_json_fn(file:  UploadFile = File(description="A file read as UploadFile")):
    
    if file.content_type != f"image/{'jpeg' or 'jpg' or 'png'}":
        raise HTTPException(400, detail="Invalid file type")
    
    with open(f"images/edge/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    path = edges(f"images/edge/{file.filename}")
    
    with open(path, "rb") as image_file:
        encoded_image_string = base64.b64encode(image_file.read())

    payload = {"mime":f"image/{file.filename.split('.')[1]}", "encoded_image":encoded_image_string}
    return payload

@app.post("/edge-file/")
async def edge_feature_file_fn(file:  UploadFile = File(description="A file read as UploadFile")):
    
    if file.content_type != f"image/{'jpeg' or 'jpg' or 'png'}":
        raise HTTPException(400, detail="Invalid file type")
    
    with open(f"images/edge/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    path = edges(f"images/edge/{file.filename}")
    
    return FileResponse(path)

@app.post("/colorfulness-file/")
async def colorfulness_file_fn(file:  UploadFile = File(description="A file read as UploadFile")):
    
    if file.content_type != f"image/{'jpeg' or 'jpg' or 'png'}":
        raise HTTPException(400, detail="Invalid file type")
    
    with open(f"{COLORFULNESS_DIR}/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    res = image_colorfulness(f"{COLORFULNESS_DIR}/{file.filename}")


    response = FileResponse(f"{COLORFULNESS_DIR}/{file.filename}", headers={"colorfulness_%":res})
    response.set_cookie(key='colorfulness_%', value=res, httponly=True)
    return response

@app.post("/colorfulness-json/")
async def colorfulness_json_fn(file:  UploadFile = File(description="A file read as UploadFile")):
    
    if file.content_type != f"image/{'jpeg' or 'jpg' or 'png'}":
        raise HTTPException(400, detail="Invalid file type")
    
    with open(f"{COLORFULNESS_DIR}/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    with open(f"{COLORFULNESS_DIR}/{file.filename}", "rb") as image_file:
        encoded_image_string = base64.b64encode(image_file.read())
    
    res = image_colorfulness(f"{COLORFULNESS_DIR}/{file.filename}")
    
    payload = {"colorfulness_%":res, "mime":f"image/{file.filename.split('.')[1]}", "encoded_image":encoded_image_string}
    return payload
