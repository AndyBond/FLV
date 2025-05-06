import tkinter as tk
from tkinter import Label
import base64
from PIL import Image, ImageTk
from io import BytesIO

# Вариант 1: Встраивание PNG файла в виде base64 строки
# Важно: Удаляем все переносы строк и пробелы из строки base64
png_base64 = """
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
root = tk.Tk()
root.title("Пример встроенного изображения в Tkinter")
root.geometry("400x300")

# Декодируем base64 строку обратно в бинарные данные
image_data = base64.b64decode(png_base64)

# Вариант 2: Чтение файла и преобразование в base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

# Использование функции для получения base64 строки из файла
# example_base64 = image_to_base64("path/to/your/image.png")

# Пример использования встроенного изображения
def use_embedded_image():
    try:
        # Создаем объект изображения из бинарных данных
        image = Image.open(BytesIO(image_data))
        
        # Теперь вы можете использовать это изображение
        width, height = image.size
        print(f"Размер изображения: {width}x{height}")
        
        # Показать изображение (если запускаете в среде, поддерживающей графику)
        # image.show()
        
        return image
    except Exception as e:
        print(f"Ошибка при открытии изображения: {e}")
        return None

# Пример вызова функции
img = use_embedded_image()
tk_image = ImageTk.PhotoImage(img)