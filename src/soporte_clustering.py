# Tratamiento de datos
# -----------------------------------------------------------------------
import numpy as np
import pandas as pd

# Otras utilidades
# -----------------------------------------------------------------------
import math
import pickle

# Para las visualizaciones
# -----------------------------------------------------------------------
import matplotlib.pyplot as plt
import seaborn as sns

# Preprocesado y modelado
# -----------------------------------------------------------------------
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

# Sacar número de clusters y métricas
# -----------------------------------------------------------------------
from yellowbrick.cluster import KElbowVisualizer
from sklearn.metrics import silhouette_score, davies_bouldin_score

# Modelos de clustering
# -----------------------------------------------------------------------
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering

# Para visualizar los dendrogramas
# -----------------------------------------------------------------------
import scipy.cluster.hierarchy as sch

class Exploracion:
    """
    Clase para realizar la exploración y visualización de datos en un DataFrame.

    Atributos:
    dataframe : pd.DataFrame
        El conjunto de datos a ser explorado y visualizado.
    """

    def __init__(self, dataframe):
        """
        Inicializa la clase Exploracion con un DataFrame.

        Params:
            - dataframe : pd.DataFrame. El DataFrame que contiene los datos a ser explorados.
        """
        self.dataframe = dataframe
    
    def explorar_datos(self):
        """
        Realiza un análisis exploratorio de un DataFrame.

        Params:
            - Ninguno.

        Returns:
            - None.
        """
        print("5 registros aleatorios:")
        display(self.dataframe.sample(5))
        print("\n")

        print("Información general del DataFrame:")
        print(self.dataframe.info())
        print("\n")

        print("Duplicados en el DataFrame:")
        print(self.dataframe.duplicated().sum())
        print("\n")

        print("Estadísticas descriptivas de las columnas numéricas:")
        display(self.dataframe.describe().T)
        print("\n")

        print("Estadísticas descriptivas de las columnas categóricas:")
        categorical_columns = self.dataframe.select_dtypes(include=['object']).columns
        if len(categorical_columns) > 0:
            display(self.dataframe[categorical_columns].describe().T)
        else:
            print("No hay columnas categóricas en el DataFrame.")
        print("\n")
        
        print("Número de valores nulos por columna:")
        print(self.dataframe.isnull().sum())
        print("\n")
        
        if len(categorical_columns) > 0:
            print("Distribución de valores categóricos:")
            for col in categorical_columns:
                print(f"\nColumna: {col}")
                print(self.dataframe[col].value_counts())
        
        print("Matriz de correlación entre variables numéricas:")
        display(self.dataframe.corr(numeric_only=True))
        print("\n")

    def visualizar_numericas(self):
        """
        Genera histogramas, boxplots y gráficos de dispersión para las variables numéricas del DataFrame.

        Params:
            - Ninguno.

        Returns:
            - None.
        """
        columns = self.dataframe.select_dtypes(include=np.number).columns

        # Histogramas
        fig, axes = plt.subplots(nrows=math.ceil(len(columns)/2), ncols=2, figsize=(21, 13))
        axes = axes.flat
        plt.suptitle("Distribución de las variables numéricas", fontsize=24)
        for indice, columna in enumerate(columns):
            sns.histplot(x=columna, data=self.dataframe, ax=axes[indice], kde=True, color="#F2C349")

        if len(columns) % 2 != 0:
            fig.delaxes(axes[-1])

        plt.tight_layout()

        # Boxplots
        fig, axes = plt.subplots(nrows=math.ceil(len(columns)/2), ncols=2, figsize=(19, 11))
        axes = axes.flat
        plt.suptitle("Boxplots de las variables numéricas", fontsize=24)
        for indice, columna in enumerate(columns):
            sns.boxplot(x=columna, data=self.dataframe, ax=axes[indice], color="#F2C349", flierprops={'markersize': 4, 'markerfacecolor': 'cyan'})
        if len(columns) % 2 != 0:
            fig.delaxes(axes[-1])
        plt.tight_layout()
    
    def visualizar_categoricas(self):
        """
        Genera gráficos de barras (count plots) para las variables categóricas del DataFrame.

        Params:
            - Ninguno.

        Returns:
            - None.
        """
        categorical_columns = self.dataframe.select_dtypes(include=['object', 'category']).columns

        if len(categorical_columns) > 0:
            try:
                _, axes = plt.subplots(nrows=len(categorical_columns), ncols=1, figsize=(15, 5 * len(categorical_columns)))
                axes = axes.flat
                plt.suptitle("Distribución de las variables categóricas", fontsize=24)
                for indice, columna in enumerate(categorical_columns):
                    sns.countplot(data=self.dataframe, x=columna, ax=axes[indice])
                    axes[indice].set_title(f'Distribución de {columna}', fontsize=20)
                    axes[indice].set_xlabel(columna, fontsize=16)
                    axes[indice].set_ylabel('Conteo', fontsize=16)
                plt.tight_layout()
            except: 
                sns.countplot(data=self.dataframe, x=categorical_columns[0])
                plt.title(f'Distribución de {categorical_columns[0]}', fontsize=20)
                plt.xlabel(categorical_columns[0], fontsize=16)
                plt.ylabel('Conteo', fontsize=16)
        else:
            print("No hay columnas categóricas en el DataFrame.")

    def visualizar_categoricas_numericas(self):
        """
        Genera gráficos de dispersión para las variables numéricas vs todas las variables categóricas.

        Params:
            - Ninguno.

        Returns:
            - None.
        """
        categorical_columns = self.dataframe.select_dtypes(include=['object', 'category']).columns
        numerical_columns = self.dataframe.select_dtypes(include=np.number).columns
        if len(categorical_columns) > 0:
            for num_col in numerical_columns:
                try:
                    _, axes = plt.subplots(nrows=len(categorical_columns), ncols=1, figsize=(10, 5 * len(categorical_columns)))
                    axes = axes.flat
                    plt.suptitle(f'Dispersión {num_col} vs variables categóricas', fontsize=24)
                    for indice, cat_col in enumerate(categorical_columns):
                        sns.scatterplot(x=num_col, y=self.dataframe.index, hue=cat_col, data=self.dataframe, ax=axes[indice])
                        axes[indice].set_xlabel(num_col, fontsize=16)
                        axes[indice].set_ylabel('Índice', fontsize=16)
                        axes[indice].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)
                    plt.tight_layout()
                except: 
                    sns.scatterplot(x=num_col, y=self.dataframe.index, hue=categorical_columns[0], data=self.dataframe)
                    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=10)
                    plt.xlabel(num_col, fontsize=16)
                    plt.ylabel('Índice', fontsize=16)
        else:
            print("No hay columnas categóricas en el DataFrame.")

    def correlacion(self, metodo="pearson", tamanio=(14, 8)):
        """
        Genera un heatmap de la matriz de correlación de las variables numéricas del DataFrame.

        Params:
            - metodo : str, optional, default: "pearson". Método para calcular la correlación.
            - tamanio : tuple of int, optional, default: (14, 8). Tamaño de la figura del heatmap.

        Returns:
            - None.
        """
        plt.figure(figsize=tamanio)
        mask = np.triu(np.ones_like(self.dataframe.corr(numeric_only=True), dtype=np.bool_))
        sns.heatmap(self.dataframe.corr(numeric_only=True, method=metodo), annot=True, cmap='viridis', vmax=1, vmin=-1, mask=mask)
        plt.title("Correlación de las variables numéricas", fontsize=24)



class Preprocesado:
    """
    Clase para realizar preprocesamiento de datos en un DataFrame.

    Atributos:
        - dataframe : pd.DataFrame. El conjunto de datos a ser preprocesado.
    """
    
    def __init__(self, dataframe, diccionario_encoding, ruta_guardar_encoder):
        """
        Inicializa la clase Preprocesado con un DataFrame.

        Params:
            - dataframe : pd.DataFrame. El DataFrame que contiene los datos a ser preprocesados.
        """
        self.dataframe = dataframe
        self.diccionario_encoding = diccionario_encoding
        self.ruta_guardar_encoder = ruta_guardar_encoder

    def standard_scaler(self):
        """
        Estandariza las columnas numéricas del DataFrame.

        Este método ajusta y transforma las columnas numéricas del DataFrame utilizando `StandardScaler` para que
        tengan media 0 y desviación estándar 1.

        Returns:
            - pd.DataFrame. El DataFrame con las columnas numéricas estandarizadas.
        """
        # Sacamos el nombre de las columnas numéricas
        col_numericas = self.dataframe.select_dtypes(include=np.number).columns

        # Inicializamos el escalador para estandarizar los datos
        scaler = StandardScaler()

        # Ajustamos los datos y los transformamos
        X_scaled = scaler.fit_transform(self.dataframe[col_numericas])

        # Sobreescribimos los valores de las columnas en el DataFrame
        self.dataframe[col_numericas] = X_scaled

        return self.dataframe
    
    def one_hot_encoding(self,nombre_encoder = "onehot_encoder.pkl", drop_index = False):
        """
        Realiza codificación one-hot en las columnas especificadas en el diccionario de codificación.

        Returns:
            - dataframe: DataFrame de pandas, el DataFrame con codificación one-hot aplicada.
        """
        # accedemos a la clave de 'onehot' para poder extraer las columnas a las que que queramos aplicar OneHot Encoding. En caso de que no exista la clave, esta variable será una lista vacía
        col_encode = self.diccionario_encoding.get("onehot", [])

        # si hay contenido en la lista 
        if col_encode:

            # instanciamos la clase de OneHot
            one_hot_encoder = OneHotEncoder(categories='auto', 
                                            drop=None, 
                                            sparse_output=True, 
                                            dtype='float', 
                                            handle_unknown='error')

            # transformamos los datos de las columnas almacenadas en la variable col_code
            trans_one_hot = one_hot_encoder.fit_transform(self.dataframe[col_encode])

            # el objeto de la transformación del OneHot es necesario convertilo a array (con el método toarray()), para luego convertilo a DataFrame
            # además, asignamos el valor de las columnas usando el método get_feature_names_out()
            oh_df = pd.DataFrame(trans_one_hot.toarray(), columns=one_hot_encoder.get_feature_names_out())

            # concatenamos los resultados obtenidos en la transformación con el DataFrame original
            if drop_index == True:
                self.dataframe = pd.concat([self.dataframe.reset_index(drop=True), oh_df.reset_index(drop=True)], axis=1)
            else:
                self.dataframe = pd.concat([self.dataframe.reset_index(drop=False), oh_df.reset_index(drop=True)], axis=1)
        
        self.dataframe.drop(columns=col_encode, inplace=True)
        # Guardar el encoder
        with open(f'{self.ruta_guardar_encoder}/{nombre_encoder}', 'wb') as f:
             pickle.dump(one_hot_encoder, f)
        return self.dataframe

    def encoding_categoricas_frequency(self, nombre_encoder = "frequency_encoder.pkl"):
        """
        Codifica las columnas categóricas del DataFrame.

        Este método reemplaza los valores de las columnas categóricas por sus frecuencias relativas dentro de cada
        columna.

        Returns:
            - pd.DataFrame. El DataFrame con las columnas categóricas codificadas.
        """

        cols_encode = self.diccionario_encoding.get("frequency", [])
        frequency_encoders = {}

        # si hay contenido en la lista 
        if cols_encode:
            # Iteramos por cada una de las columnas categóricas para aplicar el encoding
            for categoria in cols_encode:
                # Calculamos las frecuencias de cada una de las categorías
                frecuencia = self.dataframe[categoria].value_counts(normalize=True).to_dict()
                frequency_encoders[categoria] = frecuencia
                # Mapeamos los valores obtenidos en el paso anterior, sobreescribiendo la columna original
                self.dataframe[categoria] = self.dataframe[categoria].map(frecuencia)
        
        # Guardar el encoder en un archivo pickle
        with open(f'{self.ruta_guardar_encoder}/{nombre_encoder}', 'wb') as f:
            pickle.dump(frequency_encoders, f)
        
        # # Para luego llamar a este encoder y usarlo
        # with open(f'{ruta_donde_se_guardo}/{nombre_encoder}', 'rb') as f:
        #     frequency_encoders = pickle.load(f)

        # # Aplicar el encoding a un nuevo dataframe
        # for categoria, frecuencia in frequency_encoders.items():
        #     nuevo_dataframe[categoria] = nuevo_dataframe[categoria].map(frecuencia)

        return self.dataframe

class Clustering:
    """
    Clase para realizar varios métodos de clustering en un DataFrame.

    Atributos:
        - dataframe : pd.DataFrame. El conjunto de datos sobre el cual se aplicarán los métodos de clustering.
    """
    
    def __init__(self, dataframe):
        """
        Inicializa la clase Clustering con un DataFrame.

        Params:
            - dataframe : pd.DataFrame. El DataFrame que contiene los datos a los que se les aplicarán los métodos de clustering.
        """
        self.dataframe = dataframe
    
    def sacar_clusters_kmeans(self, n_clusters=(2, 15)):
        """
        Utiliza KMeans y KElbowVisualizer para determinar el número óptimo de clusters basado en la métrica de silhouette.

        Params:
            - n_clusters : tuple of int, optional, default: (2, 15). Rango de número de clusters a probar.
        
        Returns:
            None
        """
        model = KMeans()
        visualizer = KElbowVisualizer(model, k=n_clusters, metric='silhouette')
        visualizer.fit(self.dataframe)
        visualizer.show()
    
    def modelo_kmeans(self, dataframe_original, num_clusters):
        """
        Aplica KMeans al DataFrame y añade las etiquetas de clusters al DataFrame original.

        Params:
            - dataframe_original : pd.DataFrame. El DataFrame original al que se le añadirán las etiquetas de clusters.
            - num_clusters : int. Número de clusters a formar.

        Returns:
            - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de clusters.
        """
        kmeans = KMeans(n_clusters=num_clusters)
        km_fit = kmeans.fit(self.dataframe)
        labels = km_fit.labels_
        dataframe_original["clusters_kmeans"] = labels.astype(str)
        return dataframe_original, labels
    
    def visualizar_dendrogramas(self, lista_metodos=["average", "complete", "ward", "single"],grafica_size = (20, 15), titulo_size = 10):
        """
        Genera y visualiza dendrogramas para el conjunto de datos utilizando diferentes métodos de distancias.

        Params:
            - lista_metodos : list of str, optional, default: ["average", "complete", "ward"]. Lista de métodos para calcular las distancias entre los clusters. Cada método generará un dendrograma
                en un subplot diferente.

        Returns:
            None
        """
        _, axes = plt.subplots(nrows=len(lista_metodos), ncols=1, figsize=grafica_size)
        axes = axes.flat

        for indice, metodo in enumerate(lista_metodos):
            sch.dendrogram(sch.linkage(self.dataframe, method=metodo),
                           labels=self.dataframe.index, 
                           leaf_rotation=90, leaf_font_size=4,
                           ax=axes[indice])
            axes[indice].set_title(f'Dendrograma usando {metodo}',fontsize= titulo_size)
            axes[indice].set_xlabel('Muestras')
            axes[indice].set_ylabel('Distancias')
        
        plt.tight_layout()

    def plot_distribucion_clusters(self,cluster_col, grafica_size = (20,10)):
        
        columnas_plot = self.dataframe.columns.drop(cluster_col)

        fig, axes = plt.subplots(nrows=2,ncols=math.ceil(len(columnas_plot)/2),figsize = grafica_size)
        axes = axes.flat

        for indice, columna in enumerate(columnas_plot):
            df_group = self.dataframe.groupby(cluster_col)[columna].mean().reset_index()
            sns.barplot(x=cluster_col, y = columna, data = df_group,ax=axes[indice],palette="coolwarm")
            axes[indice].set_title(columna)
            plt.tight_layout()
        
        if len(columnas_plot) % 2 != 0:
            fig.delaxes(axes[-1])
        else:
            pass
        
    def radar_plot(self,cluster_col):
        # Supongamos que 'df' es tu DataFrame
        # Variables que deseas incluir en el radar plot
        variables = self.dataframe.columns.drop(cluster_col)

        # Agrupar por cluster y calcular la media
        cluster_means = self.dataframe.groupby(cluster_col)[variables].mean()

        # Repetir la primera columna al final para cerrar el radar
        cluster_means = pd.concat([cluster_means, cluster_means.iloc[:, 0:1]], axis=1)

        # Crear los ángulos para el radar plot
        num_vars = len(variables)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # Cerrar el gráfico

        # Crear el radar plot
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

        # Dibujar un gráfico para cada cluster
        for i, row in cluster_means.iterrows():
            ax.plot(angles, row, label=f'Cluster {i}')
            ax.fill(angles, row, alpha=0.25)

        # Configurar etiquetas de los ejes
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(variables)

        # Añadir leyenda y título
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.title('Radar Plot de los Clusters', size=16)
        plt.show()
        plt.tight_layout()

    def modelo_aglomerativo(self, num_clusters, metodo_distancias, metrica, dataframe_original, metricas = False, graficas = False):
        """
        Aplica clustering aglomerativo al DataFrame y añade las etiquetas de clusters al DataFrame original.

        Params:
            - num_clusters : int. Número de clusters a formar.
            - metodo_distancias ['single', 'complete', 'average', 'ward'] : str. Método para calcular las distancias entre los clusters. 
            - metrica ['euclidean', 'cosine', 'chebyshev']: str.
            - dataframe_original : pd.DataFrame. El DataFrame original al que se le añadirán las etiquetas de clusters.

        Returns:
            - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de clusters.
        """
        modelo = AgglomerativeClustering( 
            linkage=metodo_distancias,
            metric = metrica,
            distance_threshold=None,
            n_clusters=num_clusters,
        )
        # Ajustar el modelo
        aglo_fit = modelo.fit(self.dataframe)
        labels = aglo_fit.labels_
        dataframe_original["clusters_agglomerative"] = labels.astype(str)
        
        if metricas == True:
            met = self.calcular_metricas(labels)
            display(met)
        else:
            pass

        if graficas == True:
            self.plot_distribucion_clusters("clusters_agglomerative")
            self.radar_plot("clusters_agglomerative")
        return dataframe_original

    def multiples_modelos_aglomerativo(self,num_clusters=6, linkage_methods = ['single', 'complete', 'average', 'ward'], distance_metrics = ['euclidean', 'cosine', 'chebyshev'], orden = "silhouette_score", print_errors = False):
        
        results = []
        for linkage_method in linkage_methods:
            for metric in distance_metrics:
                for cluster in range(1,num_clusters+1):
                    try:
                        # Configurar el modelo de AgglomerativeClustering
                        modelo = AgglomerativeClustering(
                            linkage=linkage_method,
                            metric=metric,  #como calcula la distancia (tambien se puede llamar afinity o metric)
                            distance_threshold=None,  # Para buscar n_clusters
                            n_clusters=cluster, # Cambia esto según tu análisis
                        )

                        # Ajustar el modelo 
                        labels = modelo.fit_predict(self.dataframe)

                        # Calcular métricas si hay más de un cluster
                        if len(np.unique(labels)) > 1:
                            # Silhouette Score
                            silhouette_avg = silhouette_score(self.dataframe, labels, metric=metric)

                            # Davies-Bouldin Index
                            db_score = davies_bouldin_score(self.dataframe, labels)

                            
                            # Cardinalidad (tamaño de cada cluster)
                            cluster_cardinality = {cluster: sum(labels == cluster) for cluster in np.unique(labels)}
                        else:
                            cluster_cardinality = {0: len(self.dataframe)}
 
                        # Almacenar resultados
                        results.append({
                            'linkage': linkage_method,
                            'metric': metric,
                            'silhouette_score': silhouette_avg,
                            'davies_bouldin_index': db_score,
                            'cluster_cardinality': cluster_cardinality,
                            'n_cluster': cluster
                        })

                    except Exception as e:
                        if print_errors == True:
                            print(f"Error con linkage={linkage_method}, metric={metric}: {e}")
                        else:
                            pass
                
        # Crear DataFrame de resultados
        results_df = pd.DataFrame(results)
        # Mostrar resultados ordenados por silhouette_score
        if orden.lower() == "silhouette_score":
            results_df = results_df.sort_values(by='silhouette_score', ascending=False)
        elif orden.lower() == "davies_bouldin_index":
            results_df = results_df.sort_values(by='davies_bouldin_index', ascending=True)
        elif orden.lower() == "ambos":
            results_df = results_df.sort_values(by=['silhouette_score', 'davies_bouldin_index'], ascending=[False, True])
        return results_df

    def modelo_divisivo(self, dataframe_original, threshold=0.5, max_clusters=5):
        """
        Implementa el clustering jerárquico divisivo.

        Params:
            - dataframe_original : pd.DataFrame. El DataFrame original al que se le añadirán las etiquetas de clusters.
            - threshold : float, optional, default: 0.5. Umbral para decidir cuándo dividir un cluster.
            - max_clusters : int, optional, default: 5. Número máximo de clusters deseados.

        Returns:
            - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de los clusters.
        """
        def divisive_clustering(data, current_cluster, cluster_labels):
            # Si el número de clusters actuales es mayor o igual al máximo permitido, detener la división
            if len(set(current_cluster)) >= max_clusters:
                return current_cluster

            # Aplicar KMeans con 2 clusters
            kmeans = KMeans(n_clusters=2)
            kmeans.fit(data)
            labels = kmeans.labels_

            # Calcular la métrica de silueta para evaluar la calidad del clustering
            silhouette_avg = silhouette_score(data, labels)

            # Si la calidad del clustering es menor que el umbral o si el número de clusters excede el máximo, detener la división
            if silhouette_avg < threshold or len(set(current_cluster)) + 1 > max_clusters:
                return current_cluster

            # Crear nuevas etiquetas de clusters
            new_cluster_labels = current_cluster.copy()
            max_label = max(current_cluster)

            # Asignar nuevas etiquetas incrementadas para cada subcluster
            for label in set(labels):
                cluster_indices = np.where(labels == label)[0]
                new_label = max_label + 1 + label
                new_cluster_labels[cluster_indices] = new_label

            # Aplicar recursión para seguir dividiendo los subclusters
            for new_label in set(new_cluster_labels):
                cluster_indices = np.where(new_cluster_labels == new_label)[0]
                new_cluster_labels = divisive_clustering(data[cluster_indices], new_cluster_labels, new_cluster_labels)

            return new_cluster_labels

        # Inicializar las etiquetas de clusters con ceros
        initial_labels = np.zeros(len(self.dataframe))

        # Llamar a la función recursiva para iniciar el clustering divisivo
        final_labels = divisive_clustering(self.dataframe.values, initial_labels, initial_labels)

        # Añadir las etiquetas de clusters al DataFrame original
        dataframe_original["clusters_divisive"] = final_labels.astype(int).astype(str)

        return dataframe_original

    def modelo_espectral(self, dataframe_original, n_clusters=3, assign_labels='kmeans'):
        """
        Aplica clustering espectral al DataFrame y añade las etiquetas de clusters al DataFrame original.

        Params:
            - dataframe_original : pd.DataFrame. El DataFrame original al que se le añadirán las etiquetas de clusters.
            - n_clusters : int, optional, default: 3. Número de clusters a formar.
            - assign_labels : str, optional, default: 'kmeans'. Método para asignar etiquetas a los puntos. Puede ser 'kmeans' o 'discretize'.

        Returns:
            - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de clusters.
        """
        spectral = SpectralClustering(n_clusters=n_clusters, assign_labels=assign_labels, random_state=0)
        labels = spectral.fit_predict(self.dataframe)
        dataframe_original["clusters_spectral"] = labels.astype(str)
        return dataframe_original
    
    def modelo_dbscan(self, dataframe_original, eps_values=[0.5, 1.0, 1.5], min_samples_values=[3, 2, 1]):
        """
        Aplica DBSCAN al
          DataFrame y añade las etiquetas de clusters al DataFrame original.

        Params:
            - dataframe_original : pd.DataFrame. El DataFrame original al que se le añadirán las etiquetas de clusters.
            - eps_values : list of float, optional, default: [0.5, 1.0, 1.5]. Lista de valores para el parámetro eps de DBSCAN.
            - min_samples_values : list of int, optional, default: [3, 2, 1]. Lista de valores para el parámetro min_samples de DBSCAN.

        Returns:
            - pd.DataFrame. El DataFrame original con una nueva columna para las etiquetas de clusters.
        """
        best_eps = None
        best_min_samples = None
        best_silhouette = -1  # Usamos -1 porque la métrica de silueta varía entre -1 y 1

        # Iterar sobre diferentes combinaciones de eps y min_samples
        for eps in eps_values:
            for min_samples in min_samples_values:
                # Aplicar DBSCAN
                dbscan = DBSCAN(eps=eps, min_samples=min_samples)
                labels = dbscan.fit_predict(self.dataframe)

                # Calcular la métrica de silueta, ignorando etiquetas -1 (ruido)
                if len(set(labels)) > 1 and len(set(labels)) < len(labels):
                    silhouette = silhouette_score(self.dataframe, labels)
                else:
                    silhouette = -1

                # Mostrar resultados (opcional)
                print(f"eps: {eps}, min_samples: {min_samples}, silhouette: {silhouette}")

                # Actualizar el mejor resultado si la métrica de silueta es mejor
                if silhouette > best_silhouette:
                    best_silhouette = silhouette
                    best_eps = eps
                    best_min_samples = min_samples

        # Aplicar DBSCAN con los mejores parámetros encontrados
        best_dbscan = DBSCAN(eps=best_eps, min_samples=best_min_samples)
        best_labels = best_dbscan.fit_predict(self.dataframe)

        # Añadir los labels al DataFrame original
        dataframe_original["clusters_dbscan"] = best_labels

        return dataframe_original

    def calcular_metricas(self, labels: np.ndarray):
        """
        Calcula métricas de evaluación del clustering.
        """
        if len(set(labels)) <= 1:
            raise ValueError("El clustering debe tener al menos 2 clusters para calcular las métricas.")

        silhouette = silhouette_score(self.dataframe, labels)
        davies_bouldin = davies_bouldin_score(self.dataframe, labels)

        unique, counts = np.unique(labels, return_counts=True)
        cardinalidad = dict(zip(unique, counts))

        return pd.DataFrame({
            "silhouette_score": silhouette,
            "davies_bouldin_index": davies_bouldin,
            "cardinalidad": cardinalidad
        })