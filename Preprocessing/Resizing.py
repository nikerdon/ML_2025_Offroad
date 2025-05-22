from PIL import Image
import os

def resize_images(input_folder, output_folder, new_size=(960, 544)):
    """
    Изменяет размер всех изображений в папке input_folder и сохраняет их в output_folder.
    
    Параметры:
        input_folder (str): Путь к папке с исходными изображениями.
        output_folder (str): Путь к папке для сохранения измененных изображений.
        new_size (tuple): Новый размер изображений (ширина, высота).
    """
    # Создаем папку для результатов, если ее нет
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    k = 0 # Счётчик для вывода
    # Перебираем все файлы в папке
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                # Открываем изображение
                img_path = os.path.join(input_folder, filename)
                img = Image.open(img_path)
                
                # Изменяем размер с использованием LANCZOS (антиалиасинг)
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Сохраняем изображение
                output_path = os.path.join(output_folder, filename)
                resized_img.save(output_path)
                
                k += 1
                if (k%100 == 0):
                    print(f"{k} изображений изменено и сохранено.")
            except Exception as e:
                print(f"Ошибка при обработке изображения {filename}: {e}")

# Пример использования
input_folder = "resizing/test_input"  # Замените на ваш путь
output_folder = "resize_output"   # Замените на ваш путь

resize_images(input_folder, output_folder)