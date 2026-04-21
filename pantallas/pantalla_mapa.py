import sys
from tkinter import *
from PIL import Image, ImageTk
import os
sys.path.append('.')
from logica.personajes import buscar_personaje
from pantallas.pantalla_pelea import pantalla_batalla

def cargar_img(nombre, size=None):
    ruta = os.path.join('imgs_dissKO', nombre)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encuentra la imagen: {ruta}")
    img = Image.open(ruta)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def pantalla_mapa(root, hollows, estado, lista_personajes):
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
    def ventana_derrotado():
        canvas.unbind("<Button-1>")
        ventana_derrotado = Toplevel(root)
        ventana_derrotado.title("Hollow derrotado")
        ventana_derrotado.resizable(NO, NO)
        def volver_al_mapa():
        # Reactivamos el evento de clic en el canvas
            canvas.bind("<Button-1>", lambda e: detectar_click(e, posiciones))
            ventana_derrotado.destroy()

            # Si cierran con la "X" de la ventana, reactivamos el mapa
        ventana_derrotado.protocol("WM_DELETE_WINDOW", volver_al_mapa)

        Label(ventana_derrotado, text="¡Has derrotado a este Hollow!", font=('Arial', 16)).pack(pady=20)
    
        Button(ventana_derrotado, text="Volver al mapa", font=('Arial', 14), 
            command=volver_al_mapa).pack(pady=10)
    
    def detectar_click(event, pos, index=0):
        if index >= len(pos):
            return
        p = pos[index]
        nombre_h = p["hollow"]["nombre"]
        derrotados = estado.get("derrotados", [])
        if p["x"] <= event.x <= p["x"]+100 and p["y"] <= event.y <= p["y"]+100:
            if nombre_h not in derrotados:
                abrir_presentacion(p)
            else:
                ventana_derrotado()
            return        
        detectar_click(event, pos, index+1)

    def abrir_presentacion(hollow_info):
        canvas.unbind("<Button-1>")
        ventana = Toplevel(root)
        ventana.title("¡A LA TIRADERA!")
        ventana.resizable(NO, NO)
                                    
        def construir_equipo(nombres, index=0, resultado=None):
            if resultado is None:
                resultado = []
            if index >= len(nombres):
                return resultado
            
            p = buscar_personaje(nombres[index], lista_personajes)
            if p:
                p_nuevo = p.copy()          # Creamos una copia nueva
                p_nuevo["vida"] = p_nuevo["hp_max"] # Reseteamos la vida al máximo
                resultado.append(p_nuevo)
            return construir_equipo(nombres, index+1, resultado)
        
        def _iniciar_batalla():
            ventana.destroy()
            eq_jugador = construir_equipo(estado["personajes"])
            eq_hollow = construir_equipo([
                hollow_info["hollow"]["personaje1"],
                hollow_info["hollow"]["personaje2"],
                hollow_info["hollow"]["personaje3"]
            ])
            canvas.pack_forget()
            pantalla_batalla(root, estado, hollow_info["hollow"], eq_jugador, eq_hollow, lista_personajes)

        def re_habilitar():
            ventana.destroy()
            canvas.bind("<Button-1>", lambda e: detectar_click(e, posiciones))
        ventana.protocol("WM_DELETE_WINDOW", re_habilitar)


        Label(ventana, text=f"¡{estado['nombre']} vs {hollow_info['hollow']['nombre']}!",
            font=('Arial', 20)).pack(pady=20)
        Button(ventana, text="¡A LA TIRADERA!", font=('Arial', 16),
               command=_iniciar_batalla).pack(pady=20)

    def mostrar_hollow(pos, index=0):
        if index >= len(pos):
            return
        hollow_info = pos[index]
        nombre_h = hollow_info["hollow"]["nombre"]
        derrotados = estado.get("derrotados", [])
        if nombre_h not in derrotados:
            img_hollow = cargar_img(hollow_info["img"], size=(100, 100))
            canvas.create_image(hollow_info["x"], hollow_info["y"], anchor=NW, image=img_hollow)
            if not hasattr(canvas, 'imagenes'):
                canvas.imagenes = []
            canvas.imagenes.append(img_hollow)
        mostrar_hollow(pos, index+1)

    mostrar_hollow(posiciones)
    canvas.bind("<Button-1>", lambda e: detectar_click(e, posiciones))

    img_avatar = cargar_img(estado["avatar"], size=(80, 80))
    canvas.create_image(601, 530, anchor=NW, image=img_avatar)
    canvas.imagenes.append(img_avatar)

    