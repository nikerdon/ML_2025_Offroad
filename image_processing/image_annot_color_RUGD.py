from PIL import Image
import os

def hex_to_rgb(hex_color):
    """Конвертирует HEX-цвет (#RRGGBB) в кортеж RGB (R, G, B)."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def process_image(image_path, target_colors, unknown_colors, output_folder):
    """Обрабатывает изображение: заменяет target_colors на белый, остальное на чёрный"""
    img = Image.open(image_path)
    
    # Конвертируем в RGB, если изображение в палитровом режиме ("P") или с альфа-каналом ("RGBA")
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    pixels = img.load()
    width, height = img.size

    for x in range(width):
        for y in range(height):
            current_color = pixels[x, y]  # Теперь current_color — это кортеж (R, G, B)
            
            # Проверяем, совпадает ли пиксель с любым из target_colors
            if current_color in target_colors:
                pixels[x, y] = (255, 255, 255)  # Белый
            elif current_color in unknown_colors:
                print(image_path)
            else:
                pixels[x, y] = (0, 0, 0)  # Чёрный

    # Сохраняем в новую папку
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    img.save(output_path)
    #print(f"Обработано: {image_path} -> {output_path}")

def process_folder(input_folder, output_folder, target_hex_colors, unknown_hex_colors):
    """Обрабатывает все изображения в папке, принимая цвета в HEX."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Конвертируем HEX-цвета в RGB
    target_colors = [hex_to_rgb(color) for color in target_hex_colors]
    unknown_colors = [hex_to_rgb(color) for color in unknown_hex_colors]
    
    k = 0 # Счётчик фотографий
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(input_folder, filename)
            process_image(image_path, target_colors, unknown_colors, output_folder)
        k += 1
        if (k%100 == 0):
            print(f"Обработано {k} изображений")
    print(f"Обработка завершена. Обработано {k} изображений")

# Настройки
input_folder = "test_input1"  # Папка с исходными изображениями
output_folder = "test_output1"  # Папка для обработанных изображений
target_hex_colors = [
        "#6C4014",  #dirt
        "#FF8000",  #gravel
        "#006600" #grass (although in the village, this is not true)

        # Цвета в формате #RRGGBB
]
unknown_hex_colors = [
        "#666600",  #rock-bed
        "#994C00",  #mulch
        "#65650B", #concrete
        "#66FFFF", #bridge
        "#404040", #asphalt
        "#FFE5CC" #sand

        # Цвета в формате #RRGGBB
]

process_folder(input_folder, output_folder, target_hex_colors, unknown_hex_colors)