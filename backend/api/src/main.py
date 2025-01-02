from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import PlainTextResponse
from fastapi.encoders import jsonable_encoder
from .abc_midi import generate_midi
import tempfile
import shutil
import os

app = FastAPI(title="Partitune")
directory = os.path.join(os.path.dirname(__file__), "../files")
os.makedirs(directory, exist_ok=True)

@app.get("/iamalive")
def iamalive():
    return {"message": True}

@app.post("/generate_abc")
def generate_abc(file: UploadFile = File(...)):
    try:
        #guardar en un archivo temporal para pasarlo por partitune como archivo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".abc", dir=directory) as tf:
            shutil.copyfileobj(file.file, tf)
            temp_file_path = tf.name
            file_name = os.path.basename(temp_file_path)
        
        #file_abc = generate_abc()

        #abrir file_abc
        with open(f"{temp_file_path}", "r") as f:
            abc_content = f.read()
        
        response_data = {
            "filename": file_name,
            "content": abc_content
        }
        os.remove(temp_file_path) #borrar archivos intermedios
        return jsonable_encoder(response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating abc file.")

@app.get("/get_abc")
def get_abc(file_path:str):
    try:
        with open(f"../{file_path}", "r") as f:
            abc_content = f.read()
        return PlainTextResponse(abc_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading abc file.")

@app.get("/get_midi/{file_path}")
def get_midi(file_path: str):
    try:
        midi = os.path.join(directory, file_path)
        print(f"midi: {midi}")
        generate_midi(midi)
        output = file_path.split('.')[0]
        return FileResponse(f"{directory}/{output}.mid", media_type="audio/midi")
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")
    
