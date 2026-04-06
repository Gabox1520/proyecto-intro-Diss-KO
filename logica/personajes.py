#revisa linea por linea el documento con personajes y los añade a un diccionario
def cargar_personajes(lineas, index=0, resultado=None):
    if resultado is None:
        resultado = []
    if index >= len(lineas):
        return resultado
    linea = lineas[index].strip()
    if linea.startswith("#") or linea == "":
        return cargar_personajes(lineas, index+1, resultado)
    stats = linea.split(",")
    frases = stats[4].split("|")
    personaje = {
    "nombre": stats[0],
    "vida": int(stats[1]),
    "hp_max": int(stats[1]),
    "atk": int(stats[2]),
    "def": int(stats[3]),
    "frases": stats[4].split("|"),
    "img_icon": stats[5].strip(),
    "img_espaldas": stats[6].strip(),
    "img_frente": stats[7].strip()
}
    resultado.append(personaje)
    return cargar_personajes(lineas, index+1, resultado)

