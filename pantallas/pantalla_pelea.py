from tkinter import *
from PIL import Image, ImageTk
import os
import sys
import random
from tkinter import messagebox

sys.path.append('.')
from logica.batallas import calcular_daño, eq_derrotado, decidir_turno

def cargar_img(nombre, size=None):
    ruta = os.path.join('imgs_dissKO', nombre)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encuentra la imagen: {ruta}")
    img = Image.open(ruta)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def pantalla_batalla(root, estado, hollow, eq_jugador, eq_hollow, lista_personajes_completa):
    canvas = Canvas(root, width=1280, height=720)
    canvas.pack()
    fondo = cargar_img(hollow["fondo"], size=(1280, 720))
    canvas.create_image(0, 0, anchor=NW, image=fondo)
    canvas.fondo = fondo
    estado["puntos_jugador"] = 0
    estado["puntos_hollow"] = 0
    estado["turnos"] = 1
    #CONTADOR DE PUNTOS
    lbl_puntos = Label(canvas, 
                text=f"CAPTURAS - TÚ: 0 | HOLLOW: 0", 
                font=('Arial', 16, 'bold'), 
                bg='black', 
                fg='white',
                padx=10, pady=5)
    lbl_puntos.place(x=520, y=10)

    #CONTADOR DE TURNOS 
    lbl_turnos = Label(canvas, 
                text=f"TURNO: 1", 
                font=('Arial', 12, 'bold'), 
                bg='#333333', 
                fg='gold')
    lbl_turnos.place(x=610, y=55)

    # --- PANEL DE LOG ---
    frame_log = Frame(root, bg="#1a1a1a", bd=2, relief=SUNKEN)
    frame_log.place(x=850, y=520, width=400, height=180)
    lbl_titulo_log = Label(frame_log, text="SISTEMA DE COMBATE", font=('Arial', 10, 'bold'), bg='#333', fg='white')
    lbl_titulo_log.pack(fill=X)
    txt_historial = Label(frame_log, text="Esperando órdenes...", font=('Consolas', 10), 
                          bg="#1a1a1a", fg="#00FF00", justify=LEFT, anchor=NW, wraplength=380)
    txt_historial.pack(padx=5, pady=5, fill=BOTH)

    historial_acciones = []

    def actualizar_log(mensaje):
        historial_acciones.append(f"> {mensaje}")
        if len(historial_acciones) > 6:
            historial_acciones.pop(0)
        txt_historial.config(text="\n".join(historial_acciones))

    # --- LÓGICA DE RESTAURACIÓN (RECURSIVA) ---
    def restaurar_equipo_original(nombres, lista_completa, index=0, resultado=None):
        if resultado is None: resultado = []
        if index >= len(nombres): return resultado
        
        from logica.personajes import buscar_personaje
        # Buscamos la información base del personaje
        p_base = buscar_personaje(nombres[index], lista_completa)
        
        if p_base:
            # Creamos un diccionario NUEVO para romper cualquier vínculo con la batalla anterior
            p_limpio = p_base.copy() 
            # Forzamos que la vida sea igual al máximo
            p_limpio["vida"] = p_limpio["hp_max"] 
            resultado.append(p_limpio)
        
        return restaurar_equipo_original(nombres, lista_completa, index + 1, resultado)

    def finalizar_partida(victoria):
        if victoria:
            equipo_curado = restaurar_equipo_original(estado["personajes"], lista_personajes_completa)
            estado["equipo_actual"] = equipo_curado 
            
            if "hollows_lista" not in estado:
                from logica.hollows import cargar_hollows
                with open("data/hollows.txt", "r", encoding="utf-8") as archivo:
                    lineas_h = archivo.readlines()
                estado["hollows_lista"] = cargar_hollows(lineas_h)

            if "derrotados" not in estado:
                estado["derrotados"] = []
            nombre_hollow = hollow["nombre"]
            if nombre_hollow not in estado["derrotados"]:
                estado["derrotados"].append(nombre_hollow)

            messagebox.showinfo("¡VICTORIA!", "¡Tus personajes han recuperado energías y los Hollows capturados han vuelto a sus puestos!")
            
            canvas.destroy()
            frame_log.destroy()
            
            from pantallas.pantalla_mapa import pantalla_mapa
            # Enviamos el estado que ya tiene el "equipo_actual" curado
            pantalla_mapa(root, estado["hollows_lista"], estado, lista_personajes_completa)

    def obtener_activo(equipo, index=0):
        if index >= len(equipo): return None
        if equipo[index]["vida"] > 0: return equipo[index]
        return obtener_activo(equipo, index + 1)

    # --- ACTUALIZACIÓN DE INTERFAZ ---
    activo_j = obtener_activo(eq_jugador)
    activo_h = obtener_activo(eq_hollow)

    img_j_ref = [cargar_img(activo_j["img_espaldas"], size=(400, 400))]
    img_j_id = [canvas.create_image(100, 300, anchor=NW, image=img_j_ref[0])]
    
    img_h_ref = [cargar_img(activo_h["img_frente"], size=(400, 400))]
    img_h_id = [canvas.create_image(800, 300, anchor=NW, image=img_h_ref[0])]

    lbl_hp_j = Label(canvas, text=f"HP: {activo_j['vida']}", font=('Arial', 12), bg='black', fg='white')
    lbl_hp_j.place(x=150, y=290)
    lbl_hp_h = Label(canvas, text=f"HP: {activo_h['vida']}", font=('Arial', 12), bg='black', fg='white')
    lbl_hp_h.place(x=850, y=290)

    area_msg = Label(canvas, text="¿Qué hará el jugador?", font=('Arial', 12), bg='black', fg='white', width=40, height=3)
    area_msg.place(x=400, y=600)

    def actualizar_pantalla():
        aj = obtener_activo(eq_jugador)
        ah = obtener_activo(eq_hollow)
        if aj:
            lbl_hp_j.config(text=f"HP: {aj['vida']}")
            canvas.delete(img_j_id[0])
            img_j_ref[0] = cargar_img(aj["img_espaldas"], size=(400, 400))
            img_j_id[0] = canvas.create_image(100, 300, anchor=NW, image=img_j_ref[0])
        if ah:
            lbl_hp_h.config(text=f"HP: {ah['vida']}")
            canvas.delete(img_h_id[0])
            img_h_ref[0] = cargar_img(ah["img_frente"], size=(400, 400))
            img_h_id[0] = canvas.create_image(800, 300, anchor=NW, image=img_h_ref[0])
        p_j = estado.get("puntos_jugador", 0)
        p_h = estado.get("puntos_hollow", 0)
        t = estado.get("turnos", 1)
        
        lbl_puntos.config(text=f"CAPTURAS - TÚ: {p_j} | HOLLOW: {p_h}")
        lbl_turnos.config(text=f"TURNO: {t}")

    
    def filtrar_vivos(equipo, index=0, resultado=None):
        if resultado is None: resultado = []
        if index >= len(equipo): return resultado
        if equipo[index]["vida"] > 0: resultado.append(equipo[index])
        return filtrar_vivos(equipo, index + 1, resultado)

    def turno_hollow():
        vivos_h = filtrar_vivos(eq_hollow)
        if not vivos_h: return

        accion = random.choice(["atacar", "atacar", "cambiar"]) if len(vivos_h) > 1 else "atacar"

        if accion == "atacar":
            atc = obtener_activo(eq_hollow)
            defen = obtener_activo(eq_jugador)
            daño = calcular_daño(atc, defen)
            defen["vida"] -= daño
            frase_h = random.choice(atc["frases"])
            actualizar_log(f"{atc['nombre']}: {frase_h}")
            actualizar_log(f"Recibiste {daño} de daño")
            if defen["vida"] <= 0:
                actualizar_log(f"¡{defen['nombre']} fuera de combate!")
                actualizar_log(f"¡OH NO! {defen['nombre']} ha sido capturado.")
                estado["puntos_hollow"] += 1
                defen["vida"] = defen["hp_max"]
                eq_jugador.remove(defen)
                eq_hollow.append(defen)
        else:
            actual = obtener_activo(eq_hollow)
            def buscar_otro(vivos, exc):
                res = random.choice(vivos)
                return res if res != exc else buscar_otro(vivos, exc)
            
            nuevo = buscar_otro(vivos_h, actual)
            eq_hollow.remove(nuevo)
            eq_hollow.insert(0, nuevo) # Pasa a ser el activo
            actualizar_log(f"Hollow cambió a {nuevo['nombre']}")

    def atacar():
        aj = obtener_activo(eq_jugador)
        ah = obtener_activo(eq_hollow)
        
        # Turno Jugador
        daño = calcular_daño(aj, ah)
        ah["vida"] -= daño
        actualizar_log(f"¡Zas! {daño} de daño a {ah['nombre']}")

        # Mostrar frase del jugador en el área de mensaje
        frase_j = random.choice(aj["frases"])
        area_msg.config(text=f"{aj['nombre']}: {frase_j}")
        actualizar_log(f"{aj['nombre']} dice: {frase_j}")
        actualizar_log(f"Hiciste {daño} de daño")
        estado["turnos"] += 1
        
        if ah["vida"] <= 0:
            actualizar_log(f"¡{ah['nombre']} derrotado!")
            ah["vida"] = ah["hp_max"]
            eq_hollow.remove(ah)
            eq_jugador.append(ah) # Captura temporal
            estado["puntos_jugador"] += 1
            actualizar_log(f"¡Capturaste a {ah['nombre']}! +1 punto")

        if eq_derrotado(eq_hollow):
            actualizar_pantalla()
            finalizar_partida(True)
            return

        # Turno Hollow
        activo_h_antes = obtener_activo(eq_hollow)
        turno_hollow()

        ah_actual = obtener_activo(eq_hollow)
        if ah_actual:
            frase_h = random.choice(ah_actual["frases"])
            #las frases del Hollow también se ven en el log o área de texto
            actualizar_log(f"{ah_actual['nombre']} dice: {frase_h}")

        if eq_derrotado(eq_jugador):
            actualizar_pantalla()
            finalizar_partida(False)
            return
            
        actualizar_pantalla()

    def cambiar():
        ventana_c = Toplevel(root)
        ventana_c.title("Relevo")
        ventana_c.geometry("300x400")
        ventana_c.configure(bg="#1a1a1a")
        personaje_actual = obtener_activo(eq_jugador)

        def seleccionar(p):
            eq_jugador.remove(p)
            eq_jugador.insert(0, p)
            actualizar_log(f"¡{p['nombre']}, te toca!")
            ventana_c.destroy()
            turno_hollow()
            if eq_derrotado(eq_jugador): finalizar_partida(False)
            actualizar_pantalla()

        def crear_botones_recursivo(equipo, index=0):
            if index >= len(equipo): return
            p = equipo[index]
            if p["vida"] > 0 and p != personaje_actual:
                Button(ventana_c, text=f"{p['nombre']} (HP:{p['vida']})",
                       command=lambda sel=p: seleccionar(sel),
                       bg="#333", fg="white", width=20).pack(pady=5)
            crear_botones_recursivo(equipo, index + 1)

        crear_botones_recursivo(eq_jugador)

    btn_atacar = Button(canvas, text="ATACAR", font=('Arial', 14), bg='#1db954', fg='white', command=atacar)
    btn_atacar.place(x=400, y=650)
    btn_cambiar = Button(canvas, text="CAMBIAR", font=('Arial', 14), bg='#333', fg='white', command=cambiar)
    btn_cambiar.place(x=600, y=650)