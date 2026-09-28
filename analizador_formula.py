import re

#Importamos la lista de elementos
from elementos import ELEMENTOS

#Necesitaremos la clase atomo asi que la importamos ademas de la lista enlazada
from atomo import Atomo
from lista_enlazada import ListaEnlazada


#Funcion para analizar las partes de la formula, encontramos cuantos atomos hay de cada elelemnto
def analizar_formula(formula):

    #Con findall buscamos los simbolos de los elementos y cuanto se indica oara cada uno
    partes = re.findall(r"([A-Z][a-z]?)(\d*)", formula)

    resultado = []

    #Con un cliclo recorremos "partes"
    #y armamos el resultado con la cantidad d ecada simbolo
    for simbolo, cantidad in partes:
        if cantidad == "":
            cantidad = 1
        else:
            cantidad = int(cantidad)

        resultado.append((simbolo, cantidad))

    return resultado

#Funcion para verificar que si exista el elemento
def validar_elementos(resultado):
    for simbolo, cantidad in resultado:
        if simbolo not in ELEMENTOS:
            return False
    return True

#Necesitamos crear los objetos ATOMO para usarlos en la lista enlazada
def crear_atomos(resultado):
    atomos = []
    identificador = 1

    for simbolo, cantidad in resultado:
        nombre = ELEMENTOS[simbolo]["nombre"]
        for i in range(cantidad):
            atomo = Atomo(
                identificador,
                simbolo,
                nombre
            )

            atomos.append(atomo)
            identificador += 1

    return atomos

def crear_lista_enlazada(atomos):
    lista = ListaEnlazada()
    for atomo in atomos:
        lista.insertar(atomo)
    return lista

