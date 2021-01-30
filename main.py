from fastapi import FastAPI, File, UploadFile, Security, Depends, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from PIL import Image

import requests
import shutil

app = FastAPI()

API_KEY = "kmrhn74zgzcq4nqb"
API_KEY_NAME = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPEXCEPTION(
            status_code = HTTP_403_FORBIDDEN, detail = "Could not validate credentials"
    )

@app.post("/uploadfile/")
async def create_upload_file(api_key: APIKey = Depends(get_api_key), file1: UploadFile = File(...), file2: UploadFile = File(...)):
    fileName1 = file1.filename
    fileName2 = file2.filename

    with open("image1.jpg", "wb") as f:
        shutil.copyfileobj(file1.file, f)

    with open("image2.jpg", "wb") as g:
        shutil.copyfileobj(file2.file, g)
    
    i1 = Image.open("image1.jpg")
    i2 = Image.open("image2.jpg")

    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    diff = (dif / 255.0 * 100 / ncomponents)
    print("Difference (percentage):", )

    return {"Percent difference" : diff}