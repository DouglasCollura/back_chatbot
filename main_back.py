from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException 
from fastapi.responses import JSONResponse 
import speech_recognition as sr
from fastapi.middleware.cors import CORSMiddleware
from langchain.document_loaders import PyPDFLoader
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = sr.Recognizer()

@app.post("/upload-audio/") 

async def upload_audio(files: List[UploadFile] = File(...)): 

  for file in files:
    try:

      if file.content_type not in ["audio/webm", "audio/mpeg", "audio/mp3", "audio/wav"]: 
        raise HTTPException(status_code=422, detail="Formato de archivo no soportado")


      contents = await file.read()
      audio_path = f"uploaded_{file.filename}"
      with open(audio_path, 'wb') as f:
        f.write(contents)
      #audio_segment = AudioSegment.from_file(audio_path)
      # Convertir el audio a un formato compatible con speech_recognition 
      # wav_io = io.BytesIO() 
      # audio_segment.export(wav_io, format="wav") 
      # wav_io.seek(0)

      audio = sr.AudioFile('uploaded_audio.webm')

      with audio as source: 
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="es-ve")
      return JSONResponse(content={"message": text}, status_code=200)
    except Exception as e: 
      return JSONResponse(content={"message": str(e)}, status_code=500)
    except Exception:
      raise HTTPException(status_code=500, detail='Something went wrong')
    
    finally:
      file.close()


@app.post("/upload-file")

async def upload_file(files: List[UploadFile] = File(...)):

  for file in files:
    # loader = PyPDFLoader(r"C:\Users\Duglas\Documents\python\drylab.pdf")
    contents = await file.read()
    audio_path = f"uploaded_{file.filename}"
    with open(audio_path, 'wb') as f:
      f.write(contents)

    loader = PyPDFLoader(audio_path)
    pages=loader.load()

    return JSONResponse(content={"message": pages[2].page_content}, status_code=200)