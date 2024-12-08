# Proyecto 9: 

## 🎯 Objetivo



## Estructura del Proyecto 🗂️

```bash
Proyecto9-Clustering/
├── datos/                      # Archivos de datos CSV y PKL para el proyecto.
│   ├── 01_clustering/          # Archivos PKL de los datos para realizar los clusters.
│   ├── 02_regresiones/         # Archivos PKL de los datos para realizar las regresiones.
│   ├── 03_encoders/            # Archivos PKL de los modelos, encoders.. utilizados en los modelos.
│
├── jupyter_notebooks/          # Notebooks de Jupyter con los modelos probados.
│   ├── Modelo X/               # Carpeta del modelo
│   │   ├── 01_Clustering/      # Carpeta con lo realizado para generar los clusters
│   │   ├── 02_Regresion_Cluster_1/ # Modelos Predictivos con el Cluster 1
│   │   ├── 03_Regresion_Cluster_2/ # Modelos Predictivos con el Cluster 2
│ 
├── src/                        # Archivos .py para funciones auxiliares del proyecto.
│
└── README.md                   # Descripción del proyecto, instrucciones de instalación y uso.
```

# Instalación y Requisitos 🛠️

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instalado lo siguiente:

- **Python 3.x** 🐍
- **Jupyter Notebook** 📓 para ejecutar y visualizar los análisis de datos
- **Bibliotecas de Python**:
    - [pandas](https://pandas.pydata.org/docs/) para manipulación y análisis de datos 🧹
    - [numpy](https://numpy.org/doc/stable/) para cálculos numéricos y manejo de matrices 🔢
    - [matplotlib](https://matplotlib.org/stable/index.html) para crear gráficos básicos 📊
    - [seaborn](https://seaborn.pydata.org/) para visualizaciones estadísticas avanzadas 📈
    - [tqdm](https://tqdm.github.io/) para mostrar barras de progreso en procesos largos ⏳
    - [xgboost](https://xgboost.readthedocs.io/) para la implementación de modelos basados en Gradient Boosting 🌟
    - [scikit-learn](https://scikit-learn.org/stable/) para modelado predictivo y preprocesamiento, incluyendo:
        - `LinearRegression`, `DecisionTreeRegressor`, `RandomForestRegressor`, `GradientBoostingRegressor`, y `XGBRegressor` para tareas de regresión
        - `train_test_split`, `GridSearchCV`, `KFold`, `LeaveOneOut` y `cross_val_score` para partición de datos y validación de modelos
        - `StandardScaler` para el escalado de variables
        - Métricas como `r2_score`, `mean_squared_error`, `mean_absolute_error` para evaluar los modelos
    - [pickle](https://docs.python.org/3/library/pickle.html) para serializar y cargar modelos y objetos 🛠️

## Configuración Adicional

- Configura `pd.options.display.float_format` para un formato más claro en los valores flotantes.
- Añade rutas personalizadas al sistema usando `sys.path.append` para facilitar el acceso a los módulos personalizados del proyecto.

## Instalación 🛠️

1. Clona este repositorio para visualizarlo en vscode:
```bash
git clone https://github.com/apelsito/Proyecto9-Clustering.git
cd Proyecto9-Clustering
```

# Resumen de lo realizado en el Modelo final: 

# Resultados del Mejor Modelo (Modelo 4)
- Mejor modelo XGBooster:
- Tiene un test kappa alto.
- Mantiene un buen equilibrio entre train y test. No es overfitting.
- Es un modelo que es rápido y eficiente y nos permite ajustarle parámetros sin muchos quebraderos de cabeza.
### Métricas
![Texto alternativo](src/img/métricas%20ganadoras.png)
### Matriz Confusión
![Texto alternativo](src/img/matriz_confusion.png)
### Curva Roc
![Texto alternativo](src/img/curva_roc.png)
### Shap Plot
![Texto alternativo](src/img/shap%20plot.png)

# Conclusiones:
A partir de los resultados obtenidos podemos responder a las siguientes preguntas:

### ¿Cómo podemos agrupar a los clientes o productos de manera significativa?

Los productos los podemos agrupar por mercados en dos grupos, tenemos 4 mercados que tienen más compras que otros 3, por lo que los podemos separar en 2 grupos que contienen los siguientes mercados:
- Grupo 1: 
    - US
    - APAC
    - EU
    - LATAM
- Grupo 2:
    - Africa
    - EMEA
    - Canada

De esta forma mantenemos los datos equilibrados a la hora de realizar el análisis del profit, pero no generamos un modelo con datos demasiados disparejos que podrían dificultar las predicciones.
### ¿Qué factores son más relevantes para predecir el beneficio o las ventas dentro de cada grupo?

Esto ayudará a diseñar estrategias específicas de marketing, optimizar precios o ajustar políticas de descuento.
### ¿Cómo podemos utilizar estos insights para tomar decisiones estratégicas?

Por ejemplo, enfocarse en los segmentos más rentables o intervenir en los menos rentables.

# Contribuciones 🤝

Las contribuciones a este proyecto son muy bienvenidas. Si tienes alguna sugerencia, mejora o corrección, no dudes en ponerte en contacto o enviar tus ideas.

Cualquier tipo de contribución, ya sea en código, documentación o feedback, será valorada. ¡Gracias por tu ayuda y colaboración!

# Autores y Agradecimientos ✍️

## Autor ✒️
**Gonzalo Ruipérez Ojea** - [@apelsito](https://github.com/apelsito) en github

## Agradecimientos ❤️
Quiero expresar mi agradecimiento a **Hackio** y su equipo por brindarme la capacidad y las herramientas necesarias para realizar este proyecto con solo una semana de formación. Su apoyo ha sido clave para lograr este trabajo.
