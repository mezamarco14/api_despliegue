# Este es un comentario de prueba para el workflowaa

from flask import Flask, redirect, url_for, session, request, abort
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
import os
from datetime import datetime  # Importar datetime

app = Flask(__name__)

# Cargar las variables del archivo .env
load_dotenv()

# Configurar la clave secreta para las sesiones
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Variables de entorno para la autenticación
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = os.getenv("AUTHORITY")
REDIRECT_PATH = os.getenv("REDIRECT_PATH")
SCOPE = ["User.Read"]

# Conexión a MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)
db = client['db_Upt_Usuarios']  # Nombre de la base de datos
accesos_users_collection = db['Accesos_users']  # Nombre de la colección

# Configurar la aplicación MSAL
app_msal = ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)

@app.route('/')
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return f"Hello, {session['user']['name']}! Roles: {session.get('roles', [])}"

@app.route('/login')
def login():
    auth_url = app_msal.get_authorization_request_url(
        SCOPE,
        redirect_uri=url_for("authorized", _external=True)
    )
    print(f"Auth URL: {auth_url}")  
    return redirect(auth_url)

@app.route(REDIRECT_PATH)
def authorized():
    code = request.args.get('code')
    if not code:
        return "Error al obtener el código de autorización", 400

    result = app_msal.acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=url_for("authorized", _external=True)
    )

    if "access_token" in result:
        access_token = result['access_token']
        print(f"Access Token: {access_token}")  
        session["user"] = result.get("id_token_claims")

        # Verificar roles
        roles = result.get('id_token_claims', {}).get('roles', [])
        session['roles'] = roles

        # Guardar usuario en MongoDB
        email = session["user"].get("preferred_username")  # Asegúrate de que este campo contiene el correo
        name = session["user"].get("name")

        if email:  # Si el correo existe
            user_data = {
                "email": email,
                "name": name,
                "status": "attempted_login",  # Puedes cambiar esto a lo que necesites
                "roles": roles,
                "last_login": datetime.utcnow()  # Guardar la hora actual en UTC
            }
            # Insertar o actualizar el usuario en la base de datos
            accesos_users_collection.update_one(
                {"email": email}, 
                {"$set": user_data}, 
                upsert=True
            )
            print(f"Usuario {email} guardado/actualizado en la base de datos.")

        return redirect(url_for("index"))
    else:
        print(f"Error: {result.get('error')}, Description: {result.get('error_description')}")  
        return "Error al obtener el token de acceso", 400

@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True)
    )

@app.route('/admin')
def admin():
    if 'roles' in session and 'admin' in session['roles']:
        return "Bienvenido al área de administración."
    else:
        abort(403)  # Prohibido

@app.route('/user')
def user():
    if 'roles' in session and 'user' in session['roles']:
        return "Bienvenido al área de usuario."
    else:
        abort(403)  # Prohibido

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)