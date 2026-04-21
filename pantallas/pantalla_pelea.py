from tkinter import *
from PIL import Image, ImageTk
import os
import sys
import random
sys.path.append('.')
from logica.batallas import calcular_daño, eq_derrotado, decidir_turno, turno

def cargar_img(nombre, size=None):
    ruta = os.path.join('imgs_dissKO', nombre)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encuentra la imagen: {ruta}")
    img = Image.open(ruta)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def pantalla_batalla(root, estado, hollow, eq_jugador, eq_hollow):
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    fondo = cargar_img(hollow["fondo"], size=(1280, 720))
    canvas.create_image(0, 0, anchor=NW, image=fondo)
    canvas.fondo = fondo

    def obtener_activo(equipo, index=0):
        if index >= len(equipo):
            return None
        if equipo[index]["vida"] > 0:
            return equipo[index]
        return obtener_activo(equipo, index+1)

    activo_jugador = obtener_activo(eq_jugador)
    activo_hollow = obtener_activo(eq_hollow)

    img_jugador = cargar_img(activo_jugador["img_espaldas"], size=(400, 400))
    img_j_id = [canvas.create_image(100, 300, anchor=NW, image=img_jugador)]
    canvas.img_jugador = img_jugador

    img_hollow = cargar_img(activo_hollow["img_frente"], size=(400, 400))
    img_h_id = [canvas.create_image(800, 300, anchor=NW, image=img_hollow)]
    canvas.img_hollow = img_hollow

    Label(canvas, text=activo_jugador["nombre"], font=('Arial', 14), bg='black', fg='white').place(x=150, y=270)
    lbl_hp_jugador = Label(canvas, text=f"HP: {activo_jugador['vida']}", font=('Arial', 12), bg='black', fg='white')
    lbl_hp_jugador.place(x=150, y=290)

    Label(canvas, text=activo_hollow["nombre"], font=('Arial', 14), bg='black', fg='white').place(x=850, y=270)
    lbl_hp_hollow = Label(canvas, text=f"HP: {activo_hollow['vida']}", font=('Arial', 12), bg='black', fg='white')
    lbl_hp_hollow.place(x=850, y=290)

    puntaje = {"jugador": 0, "hollow": 0}
    lbl_puntaje = Label(canvas, text=f"Jugador: {puntaje['jugador']} | Hollow: {puntaje['hollow']}",
                        font=('Arial', 14), bg='black', fg='white')
    lbl_puntaje.place(x=540, y=20)

    area_msg = Label(canvas, text="¿Qué hará el jugador?", font=('Arial', 12),
                     bg='black', fg='white', width=40, height=3)
    area_msg.place(x=400, y=600)

    btn_atacar = Button(canvas, text="ATACAR", font=('Arial', 14), bg='#1db954', fg='white')
    btn_atacar.place(x=400, y=650)

    btn_cambiar = Button(canvas, text="CAMBIAR", font=('Arial', 14), bg='#333', fg='white')
    btn_cambiar.place(x=600, y=650)

    turno_actual = [decidir_turno()]
    contador_turno = [1]
    lbl_turno = Label(canvas, text=f"Turno: 1 | {turno_actual[0]}",
                      font=('Arial', 14), bg='black', fg='white')
    lbl_turno.place(x=540, y=50)

    def actualizar_pantalla():
        activo_j = obtener_activo(eq_jugador)
        activo_h = obtener_activo(eq_hollow)

        lbl_hp_jugador.config(text=f"HP: {activo_j['vida']}")
        lbl_hp_hollow.config(text=f"HP: {activo_h['vida']}")
        lbl_turno.config(text=f"Turno: {contador_turno[0]} | {turno_actual[0]}")
        lbl_puntaje.config(text=f"Jugador: {puntaje['jugador']} | Hollow: {puntaje['hollow']}")

        # borrar imagenes anteriores y crear nuevas
        canvas.delete(img_j_id[0])
        img_j = cargar_img(activo_j["img_espaldas"], size=(400, 400))
        img_j_id[0] = canvas.create_image(100, 300, anchor=NW, image=img_j)
        canvas.img_jugador = img_j

        canvas.delete(img_h_id[0])
        img_h = cargar_img(activo_h["img_frente"], size=(400, 400))
        img_h_id[0] = canvas.create_image(800, 300, anchor=NW, image=img_h)
        canvas.img_hollow = img_h

    def turno_hollow():
        accion = random.choice(["atacar", "cambiar"])
        if accion == "atacar":
            activo_h = obtener_activo(eq_hollow)
            activo_j = obtener_activo(eq_jugador)
            daño = calcular_daño(activo_h, activo_j)
            activo_j["vida"] -= daño
            frase = random.choice(activo_h["frases"])
            area_msg.config(text=f"Hollow: {frase}")
            if activo_j["vida"] <= 0:
                activo_j["vida"] = activo_j["hp_max"]
                eq_jugador.remove(activo_j)
                eq_hollow.append(activo_j)
                puntaje["hollow"] += 1
        else:
            area_msg.config(text="El Hollow cambió de personaje")

    def atacar():
        activo_j = obtener_activo(eq_jugador)
        activo_h = obtener_activo(eq_hollow)

        if turno_actual[0] == "jugador":
            daño = calcular_daño(activo_j, activo_h)
            activo_h["vida"] -= daño
            frase = random.choice(activo_j["frases"])
            area_msg.config(text=frase)

            if activo_h["vida"] <= 0:
                activo_h["vida"] = activo_h["hp_max"]
                eq_hollow.remove(activo_h)
                eq_jugador.append(activo_h)
                puntaje["jugador"] += 1

            if eq_derrotado(eq_hollow):
                area_msg.config(text="¡Ganaste!")
                btn_atacar.config(state=DISABLED)
                btn_cambiar.config(state=DISABLED)
                return

            turno_hollow()

            if eq_derrotado(eq_jugador):
                area_msg.config(text="¡Perdiste!")
                btn_atacar.config(state=DISABLED)
                btn_cambiar.config(state=DISABLED)
                return

        else:
            turno_hollow()

            if eq_derrotado(eq_jugador):
                area_msg.config(text="¡Perdiste!")
                btn_atacar.config(state=DISABLED)
                btn_cambiar.config(state=DISABLED)
                return

            activo_j = obtener_activo(eq_jugador)
            activo_h = obtener_activo(eq_hollow)
            daño = calcular_daño(activo_j, activo_h)
            activo_h["vida"] -= daño
            frase = random.choice(activo_j["frases"])
            area_msg.config(text=frase)

            if activo_h["vida"] <= 0:
                activo_h["vida"] = activo_h["hp_max"]
                eq_hollow.remove(activo_h)
                eq_jugador.append(activo_h)
                puntaje["jugador"] += 1

            if eq_derrotado(eq_hollow):
                area_msg.config(text="¡Ganaste!")
                btn_atacar.config(state=DISABLED)
                btn_cambiar.config(state=DISABLED)
                return

        contador_turno[0] += 1
        actualizar_pantalla()

    def cambiar():
        # cambiar consume el turno
        area_msg.config(text=f"{estado['nombre']} cambió de personaje")
        turno_hollow()

        if eq_derrotado(eq_jugador):
            area_msg.config(text="¡Perdiste!")
            btn_atacar.config(state=DISABLED)
            btn_cambiar.config(state=DISABLED)
            return

        contador_turno[0] += 1
        actualizar_pantalla()

    btn_atacar.config(command=atacar)
    btn_cambiar.config(command=cambiar)