def recomendar_componentes(presupuesto, uso, df, df_categorias, prioridades_usos):
    prioridades = prioridades_usos.get(uso, prioridades_usos['Uso General'])
    presupuesto_restante = presupuesto
    recomendaciones = []
    categorias_saltadas = []

    for categoria_nombre in prioridades:
        # Obtener el ID de la categoría
        categoria = df_categorias[df_categorias['Nombre_Categoria'] == categoria_nombre]
        if categoria.empty:
            categorias_saltadas.append(categoria_nombre)
            continue
        id_categoria = categoria.iloc[0]['ID_Categoria']

        # Filtrar productos por categoría y dentro del presupuesto
        productos_categoria = df[
            (df['ID_Categoria'] == id_categoria) &
            (df['Precio'] <= presupuesto_restante)
        ]

        if productos_categoria.empty:
            categorias_saltadas.append(categoria_nombre)
            continue

        # Seleccionar el producto más caro dentro del presupuesto
        producto_recomendado = productos_categoria.sort_values(by='Precio', ascending=False).iloc[0]

        recomendaciones.append({
            'Nombre_Producto': producto_recomendado['Nombre_Producto'],
            'Marca': producto_recomendado['Marca'],
            'Modelo': producto_recomendado['Modelo'],
            'Precio': float(producto_recomendado['Precio']),
            'Categoria': producto_recomendado['Categoria']
        })
        presupuesto_restante -= producto_recomendado['Precio']

    return recomendaciones, categorias_saltadas
