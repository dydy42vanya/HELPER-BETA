import tkinter as tk
from tkinter import PhotoImage
import os
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Communit")
root.geometry("600x600")

# Загрузка изображений
def load_image(image_name):
    image_path = os.path.join(os.path.dirname(__file__), "source", "image", image_name)
    pil_image = Image.open(image_path)
    return ImageTk.PhotoImage(pil_image)

image1 = load_image("image1.jpg")
image2 = load_image("image2.jpg")
image3 = load_image("image3.jpg")
image4 = load_image("image4.jpg")
image5 = load_image("image5.jpg")
image6 = load_image("image6.jpg")
image7 = load_image("image7.jpg")
image8 = load_image("image8.jpg")
image9 = load_image("image9.jpg")
image10 = load_image("image10.jpg")
image11 = load_image("image11.jpg")
image12 = load_image("image12.jpg")
image13 = load_image("image13.jpg")

# Создание кнопок
buttons = [
    {"text": "Геннадий Г.", "image": image1},
    {"text": "маразюк", "image": image2},
    {"text": "Megastepchik", "image": image3},
    {"text": "Ева Раттникова", "image": image4},
    {"text": "Рейн", "image": image5},
    {"text": "Денис", "image": image6},
    {"text": "ом ном", "image": image7},
    {"text": "DenCod_", "image": image8},
    {"text": "Webpma", "image": image9},
    {"text": "shiZZZoid", "image": image10},
    {"text": "Ну, Скуф (Данилл)", "image": image11},
    {"text": "天赋|D1rect9r", "image": image12},
    {"text": "Shunned", "image": image13},
]

for i, btn_data in enumerate(buttons):
    btn = tk.Button(
        root,
        text=btn_data["text"],
        compound="top",
        width=100,
        height=110,
        font=("Arial", 9),
        image=btn_data["image"]
    )

    btn.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky="w")

root.mainloop()