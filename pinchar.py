import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_image(img, title=''):
    if len(img.shape) == 3:  # Imagen a color
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img_rgb)
    else:  # Imagen en escala de grises
        plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

def pinch_transform(image, strength=0.5, radius=200):
    rows, cols, _ = image.shape
    transformed_image = np.zeros_like(image)

    center_x, center_y = cols // 2, rows // 2

    for i in range(rows):
        for j in range(cols):
            dx = j - center_x
            dy = i - center_y
            distance = np.sqrt(dx*dx + dy*dy)

            if distance < radius:
                factor = 1 - strength * (radius - distance) / radius
                new_x = int(center_x + dx * factor)
                new_y = int(center_y + dy * factor)

                if 0 <= new_x < cols and 0 <= new_y < rows:
                    transformed_image[i, j] = image[new_y, new_x]
                else:
                    transformed_image[i, j] = 0
            else:
                transformed_image[i, j] = image[i, j]

    return transformed_image

color_image = cv2.imread('IMG/cityscape.jpg')
gray_image = cv2.imread('IMG/paisaje.jpg', cv2.IMREAD_GRAYSCALE)
transformed_pinch = pinch_transform(color_image)
show_image(transformed_pinch, 'Pinch Transform')