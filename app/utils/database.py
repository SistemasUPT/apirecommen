# app/utils/database.py
import pyodbc
import pandas as pd
from app.config import Config

def obtener_datos():
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={Config.DB_SERVER};'
            f'DATABASE={Config.DB_DATABASE};'
            f'UID={Config.DB_USERNAME};'
            f'PWD={Config.DB_PASSWORD}'
        )
        productos_query = "SELECT * FROM Productos WHERE Estado_Producto = 'A'"
        categorias_query = "SELECT * FROM Categorias WHERE Estado_Categoria = 'A'"

        df_productos = pd.read_sql(productos_query, conn)
        df_categorias = pd.read_sql(categorias_query, conn)
        conn.close()

        # Unir los datos de productos y categorías
        df = df_productos.merge(df_categorias, on='ID_Categoria', how='left')
        df.rename(columns={'Nombre_Categoria': 'Categoria'}, inplace=True)

        return df, df_categorias

    except pyodbc.Error as e:
        print("Error de conexión:", e)
        return None, None
