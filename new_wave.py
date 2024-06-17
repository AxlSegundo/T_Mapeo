from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def concentric_wave_transform(image_path, output_path, amplitude, frequency):
    # Abrir la imagen con Pillow
    img = Image.open(image_path)
    img = img.convert("RGB")  # Asegurarse de que la imagen esté en formato RGB
    img_array = np.array(img)
    
    # Dimensiones de la imagen
    height, width, _ = img_array.shape
    
    # Crear un array para la imagen transformada
    wave_img_array = np.zeros_like(img_array)
    
    # Calcular el centro de la imagen
    center_x = width // 2
    center_y = height // 2
    
    # Transformación de onda concéntrica
    for y in range(height):
        for x in range(width):
            # Calcular la distancia radial desde el centro
            dx = x - center_x
            dy = y - center_y
            distance = np.sqrt(dx**2 + dy**2)
            
            # Calcular el desplazamiento de la onda
            offset = int(amplitude * np.sin(2 * np.pi * frequency * distance / width))
            
            # Coordenadas nuevas
            new_x = x + offset * (dx / distance) if distance != 0 else x
            new_y = y + offset * (dy / distance) if distance != 0 else y
            
            # Asegurarse de que las coordenadas estén dentro de los límites
            new_x = int(np.clip(new_x, 0, width - 1))
            new_y = int(np.clip(new_y, 0, height - 1))
            
            # Asignar el píxel a la nueva posición
            wave_img_array[y, x] = img_array[new_y, new_x]
    
    # Crear una nueva imagen a partir del array transformado
    wave_img = Image.fromarray(wave_img_array.astype(np.uint8))
    
    # Guardar la imagen resultante
    wave_img.save(output_path)
    
    # Mostrar la superficie deformante
    fig, ax = plt.subplots()
    ax.imshow(wave_img_array)
    plt.title(f"Transformación de Onda Concéntrica: Amplitud={amplitude}, Frecuencia={frequency}")
    plt.show()

# Ejemplo de uso
image_path = "IMG/cityscape.jpg"
output_path_1 = "IMG/imagen_transformada_onda_concentrica1.jpg"
output_path_2 = "IMG/imagen_transformada_onda_concentrica2.jpg"

# Parámetros para la segunda transformación
amplitude_2 = 50
frequency_2 = 30
concentric_wave_transform(image_path, output_path_2, amplitude_2, frequency_2)
