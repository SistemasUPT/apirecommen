# run.py
from app import create_app
import os

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    # Configurar el puerto desde la variable de entorno proporcionada por Azure
    port = int(os.environ.get("PORT", 5000))  # El puerto por defecto es 5000 si no está especificado

    # Ejecutar la aplicación en 0.0.0.0 y el puerto especificado por Azure
    app.run(debug=True, host='0.0.0.0', port=port)
