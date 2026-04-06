def cargar_hollows(lineas, index=0, resultado=None):
    if resultado is None:
        resultado = []
    if index >= len(lineas):
        return resultado
    linea = lineas[index].strip()
    if linea.startswith("#") or linea == "":
        return cargar_hollows(lineas, index+1, resultado)
    stats = linea.split(",")
    hollow = {
    "nombre": stats[0],
    "personaje1": stats[1],
    "personaje2": stats[2],
    "personaje3": stats[3],
    "fondo": stats[4].strip()
}
    resultado.append(hollow)
    return cargar_hollows(lineas, index+1, resultado)
