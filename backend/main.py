#servidor con fastapi
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from email.message import EmailMessage
import aiosmtplib
from fastapi.middleware.cors import CORSMiddleware
#------cargamos las variables de entorno .env
load_dotenv()
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))  # viene como string, convertir a int
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")
#---------

#creamos la app 
app = FastAPI()

#habilitamos cors para las peticiones del front al back
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#ruta de prueba
@app.get("/")
def home():
    return {"mensaje": "servidor corriendo con fastapi!"}

#ruta para el pedido de datos
@app.post("/send-email")
async def send_email(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    print(f"Nombre:{name}, Email: {email}, Mensaje: {message}")
    #validaciones de los campos, strip para eliminar espacios en blanco
    #si el campo esta vacio
    if not name.strip():
        return JSONResponse(content={"error": "El nombre es obligatorio."}, status_code=400)
    #si el email no tiene formato valido, aca como vemos en el string no ponemos () como una funcion por strip
    if "@" not in email:
        return JSONResponse(content={"error": "El email no es válido."}, status_code=400)
    #si el mensaje esta vacio
    if not message.strip():
        return JSONResponse(content={"error": "El mensaje es obligatorio."}, status_code=400)
    #Si todo esta bien
    print("Validaciones ok, creando email")
    #creamos el mensaje
    msg = EmailMessage()

    msg["From"] = email
    msg["To"] = EMAIL_DESTINO
    msg["Subject"] = "Nuevo mensaje de portfolio"
    msg["Reply-To"] = email
    msg.set_content(f"Nombre: {name}\nEmail: {email}\nMensaje: {message}")

    #enviamos el mensaje
    try:
        await aiosmtplib.send(
            msg,
            hostname= EMAIL_HOST,
            port=EMAIL_PORT,
            username=EMAIL_USER,
            password=EMAIL_PASS,
            use_tls=True
        )
        print("Email enviado correctamente")
        return {"mensaje":"Email enviado correctamente"}
    except Exception as e:
        print("Error al enviar email:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

