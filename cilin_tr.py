import numpy as np
import math
from PIL import Image

def cilinderX(mx, array):
    pi = math.pi
    new_array = np.zeros_like(array)
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            new_x = int(math.acos(1-(x/(mx/2))) * (mx/pi))
            new_y = y
            if new_x >= 0 and new_x < mx:
                new_array[new_x, new_y, :] = array[x, y, :]
    return new_array

def cilinderY(my, array):
    pi = math.pi
    new_array = np.zeros_like(array)
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            new_x = x
            new_y = int(math.acos(1-(y/(my/2))) * (my/pi))
            if new_y >= 0 and new_y < my:
                new_array[new_x, new_y, :] = array[x, y, :]
    return new_array

def crop_manual(image_array, start_x, start_y, end_x, end_y):
    return image_array[start_y:end_y, start_x:end_x]

def paste_manual(base_array, insert_array, start_x, start_y):
    end_x = start_x + insert_array.shape[1]
    end_y = start_y + insert_array.shape[0]
    base_array[start_y:end_y, start_x:end_x] = insert_array

def fill_black_areas(image_array):
    height, width, channels = image_array.shape
    for x in range(height):
        for y in range(width):
            if np.all(image_array[x, y] == 0):
                neighbors = []
                if x > 0 and not np.all(image_array[x-1, y] == 0):
                    neighbors.append(image_array[x-1, y])
                if x < height-1 and not np.all(image_array[x+1, y] == 0):
                    neighbors.append(image_array[x+1, y])
                if y > 0 and not np.all(image_array[x, y-1] == 0):
                    neighbors.append(image_array[x, y-1])
                if y < width-1 and not np.all(image_array[x, y+1] == 0):
                    neighbors.append(image_array[x, y+1])
                if neighbors:
                    image_array[x, y] = np.mean(neighbors, axis=0)
    return image_array

image = Image.open('IMG/cityscape.jpg')
image_array = np.array(image)

height, width, _ = image_array.shape

c1 = crop_manual(image_array, 0, 0, width//2, height//2)
c2 = crop_manual(image_array, width//2, 0, width, height//2)
c3 = crop_manual(image_array, 0, height//2, width//2, height)
c4 = crop_manual(image_array, width//2, height//2, width, height)

c1 = cilinderX(c1.shape[0], c1)
c2 = cilinderY(c2.shape[1], c2)
c3 = cilinderY(c3.shape[1], c3)
c4 = cilinderX(c4.shape[0], c4)

new_image_array = np.zeros_like(image_array)

paste_manual(new_image_array, c1, 0, 0)
paste_manual(new_image_array, c2, width//2, 0)
paste_manual(new_image_array, c3, 0, height//2)
paste_manual(new_image_array, c4, width//2, height//2)

new_image_array = fill_black_areas(new_image_array)

new_image = Image.fromarray(new_image_array)
new_image.save('IMG/imagen_transformada_cilindrica_sin_negras.jpg')
