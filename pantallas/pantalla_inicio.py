from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import sys
sys.path.append('.')
from logica.personajes import cargar_personajes
from pantallas.pantalla_mapa import pantalla_mapa
from logica.hollows import cargar_hollows

with open("data/personajes (2).txt", "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()
lista_personajes = cargar_personajes(lineas)

with open("data/hollows.txt", "r", encoding="utf-8") as archivo:
    lineas_hollows = archivo.readlines()
hollows = cargar_hollows(lineas_hollows)


def cargar_img(nombre, size=None):
    ruta = os.path.join('imgs_dissKO', nombre)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encuentra la imagen: {ruta}")
    img = Image.open(ruta)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def pantalla_inicio(root):
    estado = {"nombre": None, "avatar": None, "personajes": []}
    canvas = Canvas(root, width=1300, height=800)
    canvas.pack()
    canvas.focus_set()
    bg = cargar_img("imagen_inicio.png", size=(1300, 800))
    canvas.create_image(0, 0, anchor='nw', image=bg)
    canvas.bg = bg

    E_nombre = Entry(canvas, width=25, font=('Times New Roman', 16), bg='#2a2a2a', fg='white', bd=0)
    E_nombre.place(x=620, y=300)

    Boton_jugar = canvas.create_rectangle(335, 175, 960, 260, fill='', outline='')
    boton_info = canvas.create_rectangle(335, 455, 960, 530, fill='', outline='')
    boton_perfil = canvas.create_rectangle(335, 362, 960, 436, fill='', outline='')

    def iniciar(e):
        nombre = E_nombre.get()
        if nombre == "" and estado["avatar"] is None:
            messagebox.showwarning("Aviso", "Falta tu nombre y tu avatar")
        elif nombre == "":
            messagebox.showwarning("Aviso", "Falta tu nombre")
        elif estado["avatar"] is None:
            messagebox.showwarning("Aviso", "Falta elegir tu avatar")
        else:
            estado["nombre"] = nombre
            if len(estado["personajes"]) < 3:
                seleccion_personajes(None)
            else:
                canvas.pack_forget()
                pantalla_mapa(root, hollows, estado)

    def abrir_perfil(e):
        ventana_perfil = Toplevel(root)
        ventana_perfil.title("Elegir avatar")
        ventana_perfil.resizable(NO, NO)

        avatares = [
            "avatar_horus _fiesta.jpeg",
            "avatar_horus_audifonos.jpeg",
            "avatar_horus_dormido.jpeg"
        ]

        Label(ventana_perfil, text="Elegí tu avatar", font=('Arial', 16)).pack(pady=10)

        def elegir(av):
            estado["avatar"] = av
            ventana_perfil.destroy()

        frame = Frame(ventana_perfil)
        frame.pack()

        def mostrar_avatares(index=0):
            if index >= len(avatares):
                return
            av = avatares[index]
            img = cargar_img(av, size=(200, 200))
            btn = Button(frame, image=img, bd=2,
                        command=lambda a=av: elegir(a))
            btn.image = img
            btn.pack(side=LEFT, padx=10, pady=10)
            mostrar_avatares(index + 1)

        mostrar_avatares()

    def seleccion_personajes(e):
        ventana_perfil = Toplevel(root)
        ventana_perfil.title("Elegir personajes")
        ventana_perfil.resizable(NO, NO)

        def construir_lista(index=0, resultado=None):
            if resultado is None:
                resultado = []
            if index >= len(lista_personajes):
                return resultado
            p = lista_personajes[index]
            resultado.append((p["nombre"], p["img_icon"], p["vida"], p["atk"], p["def"]))
            return construir_lista(index+1, resultado)

        personajes = construir_lista()

        Label(ventana_perfil, text="Elegí tus personajes", font=('Arial', 16)).pack(pady=10)

        elegidos = []

        def elegir(nombre, btn):
            if nombre in elegidos:
                elegidos.remove(nombre)
                btn.config(relief=RAISED)
            elif len(elegidos) < 3:
                elegidos.append(nombre)
                btn.config(relief=SUNKEN)
            else:
                messagebox.showwarning("Aviso", "Solo podés elegir 3 personajes")

        def confirmar():
            if len(elegidos) < 3:
                messagebox.showwarning("Aviso", "Debés elegir exactamente 3 personajes")
            else:
                estado["personajes"] = elegidos
                ventana_perfil.destroy()
                root.destroy()  # cierra ventana de inicio completamente
                nuevo_root = Tk()  # crea ventana nueva
                nuevo_root.title("Mapa")
                nuevo_root.resizable(NO, NO)
                pantalla_mapa(nuevo_root, hollows, estado)
                nuevo_root.mainloop()

        frame = Frame(ventana_perfil)
        frame.pack()

        def mostrar_personajes(index=0):
            if index >= len(personajes):
                return
            nombre, img_nombre, vida, atk, defensa = personajes[index]
            img = cargar_img(img_nombre, size=(80, 80))
            btn = Button(frame, image=img, bd=2)
            btn.image = img
            btn.config(command=lambda n=nombre, b=btn: elegir(n, b))
            btn.grid(row=index//5*2, column=index%5, padx=5, pady=5)
            Label(frame, text=f"{nombre}\nHP:{vida} ATK:{atk} DEF:{defensa}",
                  font=('Arial', 8)).grid(row=index//5*2+1, column=index%5)
            mostrar_personajes(index+1)

        mostrar_personajes()
        Button(ventana_perfil, text="Confirmar", font=('Arial', 14),
               command=confirmar).pack(pady=10)

    canvas.tag_bind(Boton_jugar, "<Button-1>", iniciar)
    canvas.tag_bind(boton_info, "<Button-1>", lambda e: print("info"))
    canvas.tag_bind(boton_perfil, "<Button-1>", abrir_perfil)
    

if __name__ == "__main__":
    root = Tk()
    root.title("Inicio")
    root.resizable(NO, NO)
    pantalla_inicio(root)
    root.mainloop()