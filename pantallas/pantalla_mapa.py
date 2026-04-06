from tkinter import *
from PIL import Image, ImageTk
import os

def cargar_img(nombre, size=None):
    ruta = os.path.join('imgs_dissKO', nombre)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encuentra la imagen: {ruta}")
    img = Image.open(ruta)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def pantalla_mapa(root, hollows, estado):
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()

    fondo = cargar_img("mapa diss-KO.PNG.png", size=(1280, 720))
    canvas.create_image(0, 0, anchor=NW, image=fondo)
    canvas.fondo = fondo

    posiciones = [
        {"hollow": hollows[0], "x": 442, "y": 177, "img": "EEOO.png.png"},
        {"hollow": hollows[1], "x": 785, "y": 177, "img": "do you think about me.png.png"},
        {"hollow": hollows[2], "x": 280, "y": 320, "img": "karaoke.png.png"},
        {"hollow": hollows[3], "x": 895, "y": 360, "img": "musicalezzz.png.png"},
        {"hollow": hollows[4], "x": 360, "y": 450, "img": "nono ningun hello.png.png"},
    ]

    def mostrar_hollow(pos, index=0):
        if index >= len(pos):
            return
        hollow_info = pos[index]
        img_hollow = cargar_img(hollow_info["img"], size=(100, 100))
        canvas.create_image(hollow_info["x"], hollow_info["y"], anchor=NW, image=img_hollow)
        if not hasattr(canvas, 'imagenes'):
            canvas.imagenes = []
        canvas.imagenes.append(img_hollow)
        mostrar_hollow(pos, index+1)

    mostrar_hollow(posiciones)
    img_avatar = cargar_img(estado["avatar"], size=(80, 80))
    canvas.create_image(601, 530, anchor=NW, image=img_avatar)
    canvas.imagenes.append(img_avatar)

