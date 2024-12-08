# Modelo 1
La idea es básicamente agrupar con el mejor número de clústers y con cada grupo generar un modelo predictivo...
### Clustering
- En el análisis inicial elimino las siguientes columnas
    - ['Row ID','Order ID','Order Date','Ship Date','Customer ID','Customer Name','City','State','Country','Postal Code','Product Name']
- No voy a tocar los outliers en esta fase, considero que son datos de ventas realistas que ahora mismo buscamos agrupar en clusters
- Volvemos categoría las siguientes columnas
    - ["Ship Mode","Segment","Market","Region","Category","Sub-Category","Order Priority"]

- Realizamos Frequency Encoding a todas las columnas salvo a "Product ID"

- Utilizando Robust Scaler, aplicamos feature scaling

- Ponemos como índice la columna "Product ID"

- Realizamos un Silhoutte Score Elbow para realizar el Kmeans

- Realizamos Kmeans dividiendo en 2 grupos

- Utilizando el "Product ID" realizamos un left merge al Dataframe original de la columna "clusters_kmeans"

# Modelos de Predicción
### Fase 1: EDA y Ajuste de Datos
- Se eliminan las Columnas ['Row ID','Order ID','Order Date','Ship Date','Customer ID','Customer Name','City','State','Country','Postal Code','Product ID','Product Name']

- Se elimina Sales Tras ver las correlación

- Se convierten a tipo "category" las columnas de tipo "Object"
### Fase 2: Encoding
- Se utiliza Kruskal para medir el orden de las columnas

- Se realiza Target Encoding con las columnas ordinales

- Se realiza OneHot Encoding con las columnas nominales
### Fase 3: Feature Scaling
- Se utiliza Robust Scaler para normalizar los valores
### Fase 4: Gestión Outliers
- Se analizan pero no se gestionan en este modelo
### Fase 5: Modelos Predictivos
- Se realiza Decision Tree 

- Se realiza XGBoost

