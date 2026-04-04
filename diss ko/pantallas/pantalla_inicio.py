from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import messagebox

def cargar_img(nombre, size=None):
    ruta = os.path.join('imgs_dissKO', nombre)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encuentra la imagen: {ruta}")
    img = Image.open(ruta)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def pantalla_inicio(root):
    estado = {"nombre": None, "avatar": None}
    canvas = Canvas(root, width=1300, height=800)
    canvas.pack()
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
            print("ir al mapa con", estado)

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

    canvas.tag_bind(Boton_jugar, "<Button-1>", iniciar)
    canvas.tag_bind(boton_info, "<Button-1>", lambda e: print("info"))
    canvas.tag_bind(boton_perfil, "<Button-1>", abrir_perfil)

if __name__ == "__main__":
    root = Tk()
    root.title("Inicio")
    root.resizable(NO, NO)
    pantalla_inicio(root)
    root.mainloop()