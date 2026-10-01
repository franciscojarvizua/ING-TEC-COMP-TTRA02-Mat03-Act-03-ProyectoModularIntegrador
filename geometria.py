import math

class Geometria:
    def __init__(self, tipo, angulo):
        self.tipo = tipo
        self.angulo = angulo

    def detectar_central(self, grafo):
        candidatos = []

        for atomo, conexiones in grafo.adyacencias.items():
            if len(conexiones) == 2:
                candidatos.append(atomo)

        if len(candidatos) == 1:
            return candidatos[0]

        return None

    def detectar_extremos(self, grafo):
        central = self.detectar_central(grafo)

        if central is None:
            return []

        return grafo.adyacencias[central]

    def generar_posiciones_lineales(self, grafo, distancia=150):
        central = self.detectar_central(grafo)
        extremos = self.detectar_extremos(grafo)

        if central is None or len(extremos) != 2:
            return {}

        posiciones = {}

        posiciones[central] = (0, 0)
        posiciones[extremos[0]] = (-distancia, 0)
        posiciones[extremos[1]] = (distancia, 0)

        return posiciones

    def generar_posiciones_angulares(self, grafo, distancia=150):
        central = self.detectar_central(grafo)
        extremos = self.detectar_extremos(grafo)

        if central is None or len(extremos) != 2:
            return {}

        posiciones = {}
        posiciones[central] = (0, 0)

        mitad_angulo = self.angulo / 2
        angulo_rad = math.radians(mitad_angulo)

        x = distancia * math.sin(angulo_rad)
        y = distancia * math.cos(angulo_rad)

        posiciones[extremos[0]] = (-x, -y)
        posiciones[extremos[1]] = (x, -y)

        return posiciones

    def generar_posiciones_trigonal_plana(self, grafo, distancia=150):
        central = None

        #Detectamso el atomo con tres conexiones
        for atomo, conexiones in grafo.adyacencias.items():
            if len(conexiones) == 3:
                central = atomo
                break

        if central is None:
            return {}

        extremos = grafo.adyacencias[central]

        posiciones = {}

        posiciones[central] = (0, 0)

        angulos = [90, 210, 330]

        for atomo, angulo in zip(extremos, angulos):
            angulo_rad = math.radians(angulo)

            x= distancia * math.cos(angulo_rad)
            y = distancia * math.sin(angulo_rad)

            posiciones[atomo] = (-x, -y)

        return posiciones

    def generar_posiciones_trigonal_piramidal(self, grafo, distancia=150):
        central = None

        # Buscamos el átomo que tiene 3 conexiones
        for atomo, conexiones in grafo.adyacencias.items():
            if len(conexiones) == 3:
                central = atomo
                break

        if central is None:
            return {}

        extremos = grafo.adyacencias[central]

        posiciones = {}

        # Colocamos el átomo central
        posiciones[central] = (0, 0)

        # Ángulos para representar la base triangular
        angulos = [90, 210, 330]

        # Reducimos la distancia para dar sensación de profundidad
        distancia_base = distancia * 0.75

        for atomo, angulo in zip(extremos, angulos):
            angulo_rad = math.radians(angulo)

            x = distancia_base * math.cos(angulo_rad)
            y = distancia_base * math.sin(angulo_rad)

            posiciones[atomo] = (x, y)

        return posiciones

    def generar_posiciones_tetraedrica(self, grafo, distancia=130):
        central = None

        # Buscamos el átomo que tiene 4 conexiones
        for atomo, conexiones in grafo.adyacencias.items():
            if len(conexiones) == 4:
                central = atomo
                break

        if central is None:
            return {}

        extremos = grafo.adyacencias[central]

        posiciones = {}

        # Colocamos el átomo central
        posiciones[central] = (0, 0)

        # Posiciones para representar la geometría tetraédrica
        posiciones_extremos = [
            (0, -distancia),
            (-distancia, 0),
            (distancia, 0),
            (0, distancia)
        ]

        for atomo, posicion in zip(extremos, posiciones_extremos):
            posiciones[atomo] = posicion

        return posiciones

    def generar_posiciones_octaedrica(self, grafo, distancia=130):
        central = None

        # Buscamos el átomo que tiene 6 conexiones
        for atomo, conexiones in grafo.adyacencias.items():
            if len(conexiones) == 6:
                central = atomo
                break

        if central is None:
            return {}

        extremos = grafo.adyacencias[central]

        posiciones = {}

        # Colocamos el átomo central
        posiciones[central] = (0, 0)

        # Posiciones para representar la geometría octaédrica
        posiciones_extremos = [
            (0, -distancia),
            (0, distancia),
            (-distancia, 0),
            (distancia, 0),
            (-distancia * 0.7, -distancia * 0.7),
            (distancia * 0.7, distancia * 0.7)
        ]

        for atomo, posicion in zip(extremos, posiciones_extremos):
            posiciones[atomo] = posicion

        return posiciones




def obtener_geometria(datos_compuesto):
    tipo = datos_compuesto["geometria"]
    angulo = datos_compuesto["angulo"]

    return Geometria(tipo, angulo)

