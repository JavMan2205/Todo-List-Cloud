from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Todo List API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Tarea(BaseModel):
    titulo: str

def init_db():
    conn = sqlite3.connect("tareas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/tareas")
def obtener_tareas():
    conn = sqlite3.connect("tareas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo FROM tareas")
    filas = cursor.fetchall()
    conn.close()
    
    return [{"id": f[0], "titulo": f[1]} for f in filas]

@app.post("/tareas")
def crear_tarea(tarea: Tarea):
    if not tarea.titulo.strip():
        raise HTTPException(status_code=400, detail="El título no puede estar vacío")
        
    conn = sqlite3.connect("tareas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tareas (titulo) VALUES (?)", (tarea.titulo,))
    conn.commit()
    conn.close()
    return {"status": "Tarea guardada exitosamente"}
