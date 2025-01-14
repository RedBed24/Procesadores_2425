from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
import tempfile
import shutil
import os
from partitune.__main__ import generate_abc
import traceback

app = FastAPI(title="Partitune")
directory = os.path.join(os.path.dirname(__file__), "../files")
os.makedirs(directory, exist_ok=True)

@app.get("/iamalive")
def iamalive():
    return {"message": True}

@app.post("/generateABC")
def generateABC(file: UploadFile = File(...)):
    try:
        #guardar en un archivo temporal para pasarlo por partitune como archivo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", dir=directory) as tf:
            shutil.copyfileobj(file.file, tf)
            temp_file_path = tf.name
            file_name = os.path.basename(temp_file_path).removesuffix(".txt")
        
        generate_abc(temp_file_path) #generar archivo abc, se guarda en el mismo path pero con .abc
        path_abc = temp_file_path.removesuffix(".txt") + ".abc"
        #abrir file_abc
        with open(f"{path_abc}", "r") as f: # si no existe, lanzará excepción  = generacion no es correcta
            abc_content = f.read()
        
        with open("partitune.log", "r") as f:
            warnings = [line.split("WARNING - ")[1] for line in f if "WARNING - " in line]

        response_data = {
            "filename": file_name,
            "content": abc_content,
            "warnings": "\n".join(warnings)
        }
        os.remove(temp_file_path) #borrar archivos intermedios
        os.remove(path_abc)
        return jsonable_encoder(response_data)
    except Exception as e:
        traceback.print_exc()
        with open("partitune.log", "r") as f:
            error_messages =  [line.split("ERROR - ")[1] for line in f if "ERROR - " in line]
            warnings = [line.split("WARNING - ")[1] for line in f if "WARNING - " in line]
        if len(error_messages) == 0:
            error_messages = ["An unexpected error occurred"]
        raise HTTPException(status_code=500, detail="\n".join(error_messages + warnings))

