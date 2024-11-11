# app/routes/recommend.py
from flask import Blueprint, request, jsonify
from app.utils.database import obtener_datos  # Asegúrate de que esta importación sea correcta
from app.utils.recommendation import recomendar_componentes

bp = Blueprint('recommend', __name__)

# Resto del código

PRIORIDADES_USOS = {
    'Gaming': ['Tarjeta Gráfica', 'Procesador', 'RAM', 'Almacenamiento', 'Placa Madre', 'Fuente de poder', 'Refrigeración', 'Caja'],
    'Edición de Video': ['Procesador', 'RAM', 'Almacenamiento', 'Tarjeta Gráfica', 'Placa Madre', 'Fuente de poder', 'Refrigeración', 'Caja'],
    'Trabajo de Oficina': ['Procesador', 'RAM', 'Almacenamiento', 'Placa Madre', 'Fuente de poder', 'Caja'],
    'Desarrollo de Software': ['Procesador', 'RAM', 'Almacenamiento', 'Placa Madre', 'Fuente de poder', 'Caja'],
    'Uso General': ['Procesador', 'RAM', 'Almacenamiento', 'Placa Madre', 'Fuente de poder', 'Caja']
}

@bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()

    # Validar la entrada
    if not data:
        return jsonify({'error': 'Solicitud vacía.'}), 400

    presupuesto = data.get('presupuesto')
    uso = data.get('uso')

    if presupuesto is None or uso is None:
        return jsonify({'error': 'Faltan parámetros: presupuesto y uso son obligatorios.'}), 400

    # Validar tipos de datos
    try:
        presupuesto = float(presupuesto)
    except ValueError:
        return jsonify({'error': 'El presupuesto debe ser un número.'}), 400

    if uso not in PRIORIDADES_USOS:
        return jsonify({'error': f'Uso no válido. Los usos válidos son: {list(PRIORIDADES_USOS.keys())}'}), 400

    # Obtener datos
    df, df_categorias = obtener_datos()
    if df is None or df_categorias is None:
        return jsonify({'error': 'Error al obtener datos de la base de datos.'}), 500

    # Generar recomendaciones
    recomendaciones, categorias_saltadas = recomendar_componentes(presupuesto, uso, df, df_categorias, PRIORIDADES_USOS)

    if not recomendaciones:
        return jsonify({
            'message': 'No se encontraron componentes que se ajusten al presupuesto y uso especificado.'
        }), 200

    response = {
        'recomendaciones': recomendaciones
    }

    if categorias_saltadas:
        response['advertencia'] = {
            'mensaje': 'El presupuesto no fue suficiente para recomendar componentes en las siguientes categorías.',
            'categorias': categorias_saltadas,
            'sugerencia': 'Considera aumentar tu presupuesto para cubrir todas las categorías prioritarias.'
        }

    return jsonify(response), 200

@bp.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'API de Recomendación de Componentes de Hardware',
        'endpoints': {
            '/recommend': 'POST'
        }
    }), 200
