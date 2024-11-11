import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde el archivo .env

class Config:
    DB_SERVER = os.getenv('DB_SERVER', 'dbpoma.database.windows.net')
    DB_DATABASE = os.getenv('DB_DATABASE', 'db_lakume')
    DB_USERNAME = os.getenv('DB_USERNAME', 'jhonpoma')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'UPT.2024')
