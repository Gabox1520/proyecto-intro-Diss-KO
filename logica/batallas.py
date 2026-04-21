import random
def decidir_turno():
    return random.choice(["jugador", "Hollow"])
def calcular_daño(atacante, defensor):
    daño=atacante["atk"]-defensor["def"]
    if daño<1:
        daño=1
    return daño
#revisa si el equipo está derrotado(si todos sus personajes tienen vida 0)
def eq_derrotado(equipo, index=0):
    if index>=len(equipo):
        return True
    if equipo[index]["vida"]>0:
        return False
    return eq_derrotado(equipo, index+1)
#define el turno en la batalla, cambia cada que termina el turno y lleva un contador de turnos
def turno(atacante, defensor, eq_atc, eq_def, turno_jug, turno_num=0):
    if eq_derrotado(eq_def):
        ganador = "jugador" if turno_jug == "jugador" else "Hollow"
        return {"ganador": ganador, "turno": turno_num}
    if eq_derrotado(eq_atc):
        ganador = "Hollow" if turno_jug == "jugador" else "jugador"
        return {"ganador": ganador, "turno": turno_num}
    daño = calcular_daño(atacante, defensor)
    defensor["vida"] -= daño
    if defensor["vida"] <= 0:
       defensor["vida"] = defensor["hp_max"]
       eq_def.remove(defensor)
       eq_atc.append(defensor)
    return turno(defensor, atacante, eq_def, eq_atc, "Hollow" if turno_jug == "jugador" else "jugador", turno_num+1)
