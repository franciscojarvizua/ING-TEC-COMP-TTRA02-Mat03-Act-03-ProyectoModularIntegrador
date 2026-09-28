
class Grafo:
    #Creamos la relación que hay entre los atomos mediante un alista de adyacencias
    def __init__(self):
        self.adyacencias = {}

    #Buscamos y agregamso cada atomo al grafo
    def agregar_atomo(self, atomo):
        self.adyacencias[atomo.identificador] = []

    #Una vez establcida la relacion agregamos los atomos relacionados
    def agregar_atomos(self, atomos):
        for atomo in atomos:
            self.agregar_atomo(atomo)

    #Con base en lo anterior creamos el enlace entre los atomos en cuestion
    def agregar_enlace(self, atomo1, atomo2):
        self.adyacencias[atomo1.identificador].append(atomo2.identificador)
        self.adyacencias[atomo2.identificador].append(atomo1.identificador)

    #La conexion esta preestablecida en la lista de compuestos
    def agregar_conexiones(self, atomos, conexiones):
        for id1, id2 in conexiones:
            #Le restamos 1 por motivo del indice o posicion cero
            atomo1 = atomos[id1-1]
            atomo2 = atomos[id2 - 1]
            self.agregar_enlace(atomo1, atomo2)

    #Mostramos las conexiones de manera visual
    def mostrar(self):
        for atomo, conexiones in self.adyacencias.items():
            print(atomo, "->", conexiones)

    #contamos tambien la cantidad de enlaces
    def cantidad_enlaces(self):
        total = 0
        for conexiones in self.adyacencias.values():
            total += len(conexiones)
        return total // 2
