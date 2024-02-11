

# %%
import numpy as np
from itertools import product
import pickle
import json
import os
scales = [{"name": "Escala Mayor", "root": 0, "intervals": [0, 2, 4, 5, 7, 9, 11]},
    {"name": "Escala Menor ", "root": 0, "intervals": [0, 2, 3, 5, 7, 8, 10]},
    {"name": "Escala Pentatónica Mayor", "root": 0, "intervals": [0, 2, 4, 7, 9]},
    {"name": "Escala Pentatónica Menor", "root": 0, "intervals": [0, 3, 5, 7, 10]},
    {"name": "Escala Armónica Menor", "root": 0, "intervals": [0, 2, 3, 5, 7, 8, 11]},
    {"name": "Escala Melódica Menor", "root": 0, "intervals": [0, 2, 3, 5, 7, 9, 11]},
    {"name": "Escala Dórica", "root": 0, "intervals": [0, 2, 3, 5, 7, 9, 10]},
    {"name": "Escala Frigia", "root": 0, "intervals": [0, 1, 3, 5, 7, 8, 10]},
    {"name": "Escala lydia", "root": 0, "intervals": [0, 2, 4, 6, 7, 9, 11]},
    {"name": "Escala Mixolidia", "root": 0, "intervals": [0, 2, 4, 5, 7, 9, 10]},
    {"name": "Escala Locria", "root": 0, "intervals": [0, 1, 3, 5, 6, 8, 10]},
    {"name": "Escala Alterada", "root": 0, "intervals": [0, 1, 3, 4, 6, 8, 10, 11]}
]

# %%
def generate_chords(scale, octaves, sizes, intervals, max_population=-1):
    """
    Genera una lista de acordes musicales.

    Parámetros:
    - scale: un diccionario que representa la escala musical. Debe contener 'intervals' y 'root'.
    - octaves: una lista de octavas en las que se generarán los acordes.
    - sizes: una lista de tamaños de acorde (número de notas en el acorde).
    - intervals: una lista de intervalos musicales posibles para los acordes.
    - max_population: número máximo de acordes a generar. Si es -1, no hay límite.

    Retorna:
    - Una lista de diccionarios, donde cada diccionario representa un acorde.
    """

    chords = []  # Lista para almacenar los acordes generados

    # Itera sobre cada octava proporcionada
    for octave in octaves:
        # Itera sobre cada nota de la escala
        for index, note in enumerate(scale["intervals"]):
            # Itera sobre los tamaños de acorde dados
            for size in sizes:
                # Crea todas las combinaciones posibles de intervalos para el tamaño actual
                for interval_permutation in product(intervals, repeat=size):
                    # Construye el acorde inicial con su octava, nota raíz e intervalos
                    chord = {"octave": octave, "root": scale["root"] + note, "intervals": list(interval_permutation)}

                    pos = index  # Posición actual en la escala
                    # Actualiza los intervalos del acorde basándose en la escala
                    for i, interval in enumerate(chord["intervals"]):
                        val = (pos + chord["intervals"][i]) % len(scale["intervals"])
                        chord["intervals"][i] = (scale["intervals"][val] - scale["intervals"][pos]) % 12
                        pos = val

                    # Añade el acorde a la lista de acordes
                    chords.append(chord)

                    # Si se alcanza la población máxima de acordes, termina el bucle
                    if max_population > 0 and len(chords) == max_population:
                        break

    return chords  # Devuelve la lista de acordes generados

# %%
selected_scale = scales[0]  # fijar la escala de generacion

chords = generate_chords(selected_scale, [5], [2], [2], -1)  # Genera hasta 3 acordes de longitud 2 con intervalos de 2 o 3 saltos en la escala

for chord in chords:
    print(chord)

# %%
def create_experiment_data(scale, octaves, sizes, intervals, chords):
    """
    Crea un diccionario con los datos de un experimento musical.

    Parámetros:
    scale: Diccionario que representa la escala musical.
    octaves: Lista de octavas para generar acordes.
    sizes: Lista de tamaños de los acordes.
    intervals: Lista de intervalos para los acordes.
    chords: Lista de acordes generados.

    Retorna:
    Diccionario con los datos del experimento.
    """
    # Aquí podrías añadir validaciones para los parámetros

    experiment_name = f'Experimento PC set - {scale["name"]}'
    return {
        'experiment_name': experiment_name,
        'experiment_params': {
            'scale': scale,
            'octaves': octaves,
            'sizes': sizes,
            'intervals': intervals
        },
        'chords': chords
    }

# Uso de la función
experiment_data = create_experiment_data(selected_scale, [5], [2], [2], chords)


# %%
# Asegurarse de que los datos del experimento están presentes
if 'experiment_name' in experiment_data and 'experiment_params' in experiment_data:
    # Extraer los parámetros necesarios del diccionario de datos del experimento
    experiment_name = experiment_data['experiment_name']
    octaves = experiment_data['experiment_params']['octaves']
    intervals = experiment_data['experiment_params']['intervals']

    # Crear el nombre de la carpeta basado en los detalles del experimento
    folder_name = f'{experiment_name} - Octava {octaves[0]} - Intervalos {intervals[0]}'

    # Construir la ruta completa de la carpeta
    folder_path = os.path.join(r"C:\Users\SANTIAGO\Documents\GitHub\Trabajo de Grado Master\DATA", folder_name)

else:
    raise ValueError("Los datos del experimento no están completos o son incorrectos")

# Aquí puedes continuar con el código para usar 'folder_path', por ejemplo, para guardar datos


# %%
# Asumiendo que 'folder_path' ya ha sido definido previamente

# Crear la carpeta si no existe
try:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Nota: os.makedirs ya verifica si la carpeta existe antes de crearla,
    # pero esta comprobación adicional permite manejar la lógica de forma más explícita
except Exception as e:
    # Manejar cualquier excepción que pueda surgir al crear la carpeta
    print(f"Error al crear la carpeta: {e}")
    # Aquí podrías decidir si lanzar la excepción o manejarla de otra manera

# Guardar los datos del experimento en un archivo pickle dentro de la nueva carpeta
try:
    with open(os.path.join(folder_path, 'experiment_data.pkl'), 'wb') as f:
        pickle.dump(experiment_data, f)
except Exception as e:
    # Manejar cualquier excepción que pueda surgir al guardar los datos
    print(f"Error al guardar los datos del experimento: {e}")




# %%
