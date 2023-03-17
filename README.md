# Image Proecessing API

A simple api to to extract features from your image, built with python and FastAPI.

## Core functionality
- Intensity Features
- Edge Features
- Colour Intensity
- Image Colourfulness

## How To Run
The main thing you need to run FastAPI application in a remote server machine is an ASGI server program like `UVICORN`
In the directory where you the `main.py file` RUN:
`uvicorn main:app --host="0.0.0.0" --port=8000`



## End Points
There are Seven End-Points in total, Details Below;

### 1. Home / Welcome End-Point

    url = "http://0.0.0.0:8000/"
    res = requests.request("GET", url, data=payload, headers=headers)

### 2. Colour Content

2.1

    url = "http://0.0.0.0:8000/color-content-file/"
    payload = "SOME IMAGE FILE"
    res = requests.request("POST", url, data=payload)

    returns an image file reponse with the processed result stored in the cookies and headers of the response object.

2.2 

    url = "http://0.0.0.0:8000/color-content-json/"
    payload = "SOME IMAGE FILE"
    res = requests.request("POST", url, data=payload)

    returns the result in JSON form reponse with the image encoded in base64 inside the json object(decode the string to get back the image).

### 3. Colorfulness

3.1

    url = "http://0.0.0.0:8000/colorfulness-file/"
    payload = "SOME IMAGE FILE"
    response = requests.request("POST", url, data=payload)

    returns an image file reponse with the processed result stored in the cookies and headers of the response object.

3.2

    url = "http://0.0.0.0:8000/colorfulness-json/"
    payload = "SOME IMAGE FILE"
    response = requests.request("POST", url, data=payload)

    returns the result in JSON form reponse with the image encoded in base64 inside the json object(decode the string to get back the image).

### 3. Edge Features

3.1

    url = "http://0.0.0.0:8000/edge-file/"
    payload = "SOME IMAGE FILE"
    response = requests.request("POST", url, data=payload, headers=headers)

    returns an image file reponse with the processed result stored in the cookies and headers of the response object.

3.2

    url = "http://0.0.0.0:8000/edge-json/"
    payload = "SOME IMAGE FILE"
    response = requests.request("POST", url, data=payload)

    returns the result in JSON form reponse with the image encoded in base64 inside the json object(decode the string to get back the image).

## Extra 
how to decode base64 image string
img_data = "endcoded string in base64"

with open("imageToSave.jpg", "wb") as fh:
    fh.write(img_data.decode('base64'))

# THE END
