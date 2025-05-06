import tkinter as tk
from tkinter import Label
import base64
from PIL import Image, ImageTk
from io import BytesIO

# Правильный пример base64 PNG изображения (маленький цветной квадрат)
# Важно: удалены все переносы строк для предотвращения ошибок декодирования
png_base64 = png_base64 = """
iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAE
    m0lEQVR4nO2ZW4hVVRjHf3PmzHhGZ7x0UZuaVCQLL5CoKZKFDxLlBcMeehDzQpE4iU9FpERPYWUP
    QpRgZGYPmViRpCVeCnUULyiKWpqKWmrq6Gi3M+PpYa09Z83es9c+e8Y5ExH7h8We2d/6vv3/vrX2
    2mvtDeWUU04DWpLv4H0LgKnACGAoUAWMAQYDlcAA066lpHXAb8AZ4DJwFqgHjgHHgYaibTmrNwlY
    DnwD/AEYn58B9gKfARFwoL8dGA/cC7wEHARu+gRshNzfwPdALbAYGOsbvD8c6AkOQRxiFLAI2CGZ
    9BH7KrAZeAiojM/5clAGGkTuHYF74KmSbJsEHgI+AS55BIwLfx7YAEz3BeqvFzGQBgwFngC+FIGd
    4L8BzwF16UDdwfRTUDOAb4FrjnDNwBvAeE8fFuiDYXWAGhJgqQG8Adwa3WEgBIbJoFanFxjSKAVs
    kGSqALcBa4BWR0rbBqwABnYnUKEODCwz/CTwCLDKk+Fm4EEzO0WWQlpA6oEnTXpTEg21EfKi7D4s
    AXPSQdJ6gCpgFnCyhM2s2Fbs+xD9BGYW6wHp3k4A7cCnZqYZAfwcgAMrgPXmf4NsQvYD02QZTL2I
    xaT7eICsUdMi86xUJ56VLHY2Jn9HJUhW4A44jlAgtwI1sr7bQdcBrxVwoAa427SPgSw2fdJ60C9y
    m4EnzP2QlCy22fWXdOfFWK11ZjZpB14F7vNNh6SbbPtjqZHHAYdM22a586W1jx1olhK7S8rrcRHw
    qy8nQfHABHDIFbCUA53mQk/0XWVRUcqukeWrXe4ugMfN/cvx+icdaAUOSKyVaexCaF5DcM1kVFGy
    UHuO7KYM/KIsNV3JY4/rwFXgRzLfpBQhIXRzinagPfXwJTLbkZSnX0pS3lzp4CnFSd7LN/MkZZur
    vE5PBzrMhXrUNQXSpQYsAE4H4sB1cyCbNV8Hkgt17b29j+Wt+YoAHEiU12nVgXTVGWkm+i77BFXj
    kxmDdzlwMudWnGvPcUC+KoGVwLm9cCBrz3Fg1F4EH58yuDdKOFApr+hWqGXUgYZqY/BGSQdGywu4
    3VUH3ClUs88BRWocKJlChzV66qVQFTILDQuJYQV+qZPWAeW9H2RiP8PO75JCRqtldHpoBQzQVJtd
    8mFTGXqXHCxEaB1oJmPmfFZUZWxrdLrr3UWhXdkRtbK6tMk5Hj9Ip8GejRFPxnzDGJdPw8ivXhsy
    nYAmuXKK7I7uEFnS3uGYdZrk4yHOHR1NJiRfjsYvldJxjwVwRLmfXeHSdUb2XMuyAy3KrPuHY2dg
    ZUP6i1vboV0/uYI7Q2O2dUadGKmWy8v5Np1Z2sJLpVk+iG9OdaRzRopdoVr547v+s92iXG7MZPdZ
    B5qUWI8Z9YSbvvmP44h5wWtJBSl1KvKoO9hXtBN4hDR6C7ygpFGk0QplIPSJIiUVp1ZZ0jXKkq7V
    k7JOUqelQAXVOrw4tF+5aG9jYyS+bJRk5+NCXEhsLLJhbIvHAg7Ycw/YZnbwESHngbaSMZZLxmy0
    n1AayJ6YOtBYgrHegT5jHDu3Lhn9rXTgQAnaIdsgD+fDPAjKKaecAaX/AJSXbVW6JxvAAAAAAElF
    TkSuQmCC
""".replace("\n", "").strip()
def use_embedded_image(img_base64):
    try:
        # Декодируем base64 строку обратно в бинарные данные
        image_data = base64.b64decode(img_base64)
        
        # Создаем объект изображения из бинарных данных
        image = Image.open(BytesIO(image_data))
        
        # Теперь вы можете использовать это изображение
        width, height = image.size
        print(f"Размер изображения: {width}x{height}")
        print(f"Формат изображения: {image.format}")
        
        # Показать изображение (если запускаете в среде, поддерживающей графику)
        # image.show()
        
        return image
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

def b64_to_bin(img_base64):
    try:
        image_data = base64.b64decode(img_base64)
        return image_data
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

# Функция для конвертации существующего файла PNG в base64 строку
def image_to_base64_string(image_path):
    try:
        with open(image_path, "rb") as image_file:
            # Читаем бинарные данные
            binary_data = image_file.read()
            # Кодируем в base64
            encoded_data = base64.b64encode(binary_data)
            # Конвертируем байты в строку
            base64_string = encoded_data.decode('utf-8')
            
            print(f"Длина base64 строки: {len(base64_string)}")
            return base64_string
    
    except Exception as e:
        print(f"Ошибка при конвертации изображения: {e}")
        return None

# Функция для сохранения base64 строки в файл для проверки
def save_base64_to_image(base64_string, output_path):
    try:
        # Декодируем строку
        image_data = base64.b64decode(base64_string)
        
        # Сохраняем бинарные данные в файл
        with open(output_path, "wb") as file:
            file.write(image_data)
            
        print(f"Изображение сохранено в {output_path}")
        return True
    
    except Exception as e:
        print(f"Ошибка при сохранении изображения: {e}")
        return False
filename = "splash"
pngfilename = filename + ".png"
b64gilename = filename + ".b64"

# Пример использования
i = image_to_base64_string('images\\' + pngfilename)
print(i)
with open(b64gilename, "w") as f:
  f.write(i)
img = use_embedded_image(i)
root = tk.Tk()
b = b64_to_bin(i)
root.tk_image = ImageTk.PhotoImage(Image.open(BytesIO(b)))

canvas = tk.Canvas(root, width = 600, height = 600)
canvas.pack()
canvas.create_image(20, 20, anchor=tk.NW, image=root.tk_image)
root.mainloop()

#root.tk_image = ImageTk.PhotoImage(i)
#save_base64_to_image(i, 'images\\i2.png')

# Если у вас есть файл PNG, вы можете преобразовать его в base64 строку:
# base64_str = image_to_base64_string("your_image.png")
# print(base64_str)  # Вы можете скопировать эту строку и вставить в ваш код

# Для проверки корректности base64 строки:
# save_base64_to_image(png_base64, "test_output.png")1