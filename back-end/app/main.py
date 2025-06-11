from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ⬅️ Importar CORS
from app.database import engine, Base
from app.routers import  Localidades, Companies, Colaborators
import time
from sqlalchemy.exc import OperationalError

app = FastAPI()

# ✅ Habilitar CORS
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🔁 Espera activa a que la base de datos esté lista
max_retries = 20
for attempt in range(max_retries):
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos lista.")
        break
    except OperationalError:
        wait_time = 2
        print(f"⏳ Esperando conexión a la base de datos... Intento {attempt+1}/{max_retries}")
        time.sleep(wait_time)
else:
    raise Exception("❌ No se pudo conectar a la base de datos después de varios intentos.")

# 📦 Rutas
#app.include_router(items.router)
app.include_router(Localidades.router)
app.include_router(Companies.router)
app.include_router(Colaborators.router)