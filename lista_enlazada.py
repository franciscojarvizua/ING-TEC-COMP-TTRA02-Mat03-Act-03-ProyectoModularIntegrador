class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def insertar(self, dato):
        nuevo_nodo = Nodo(dato)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            nodo_actual = self.cabeza
            while nodo_actual.siguiente is not None:
                nodo_actual = nodo_actual.siguiente

            nodo_actual.siguiente = nuevo_nodo

    def recorrer(self):
        nodo_actual = self.cabeza
        while nodo_actual is not None:
            print(
                nodo_actual.dato.identificador,
                nodo_actual.dato.simbolo,
                nodo_actual.dato.nombre
            )
            nodo_actual = nodo_actual.siguiente

    def cantidad(self):
        contador = 0
        nodo_actual = self.cabeza

        while nodo_actual is not None:
            contador += 1
            nodo_actual = nodo_actual.siguiente

        return contador

