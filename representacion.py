import tkinter as tk

class Representacion:
    def __init__ (self, canvas):
        self.canvas = canvas
    #Dinujamos el circulo que representara a cada atomo
    def dibujar_atomo(self, x, y, simbolo):
        radio = 25

        self.canvas.create_oval(
            x - radio,
            y - radio,
            x + radio,
            y + radio
        )

        self.canvas.create_text(
            x,
            y,
            text=simbolo,
            font=("Arial", 14, "bold")
        )

    #Adibujamos las lineas que representaran los enlaces
    def dibujar_enlace(self, x1, y1, x2, y2):
        radio = 25

        dx = x2 - x1
        dy = y2 - y1

        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia == 0:
            return

        direccion_x = dx / distancia
        direccion_y = dy / distancia

        inicio_x = x1 + direccion_x * radio
        inicio_y = y1 + direccion_y * radio

        final_x = x2 - direccion_x * radio
        final_y = y2 - direccion_y * radio

        self.canvas.create_line(
            inicio_x,
            inicio_y,
            final_x,
            final_y,
            width=3
        )

    #Aqui armamos la scaracteristicas del dibujo de la molecula
    def dibujar_molecula(
        self,
        atomos,
        grafo,
        posiciones,
        centro_x=300,
        centro_y=200
    ):

        # Dejamos limpio el canvas
        self.canvas.delete("all")

        # A cada atomo lo identificamos y registramos en un disccioanrio
        atomos_por_id = {}

        for atomo in atomos:
            atomos_por_id[atomo.identificador] = atomo

        if not posiciones:
            return

        #Obtenemos loslimites de la molecula
        valores_x = []
        valores_y = []

        for x, y in posiciones.values():
            valores_x.append(x)
            valores_y.append(y)

        minimo_x = min(valores_x)
        maximo_x = max(valores_x)

        minimo_y = min(valores_y)
        maximo_y = max(valores_y)

        ancho_molecula = maximo_x - minimo_x
        alto_molecula = maximo_y - minimo_y

        # Tamaño del canvas
        ancho_canvas = int(self.canvas["width"])
        alto_canvas = int(self.canvas["height"])

        # Dejamos un margen para que los átomos no queden pegados al borde
        margen = 60

        ancho_disponible = ancho_canvas - margen
        alto_disponible = alto_canvas - margen

        # Determinamos una escala
        escala_x = 1

        if ancho_molecula > 0:
            escala_x = ancho_disponible / ancho_molecula

        escala_y = 1

        if alto_molecula > 0:
            escala_y = alto_disponible / alto_molecula

        # Utilizamos la escala más pequeña para mantener las proporciones
        escala = min(escala_x, escala_y, 1)

        # Calculamos el centro
        centro_molecula_x = (minimo_x + maximo_x) / 2
        centro_molecula_y = (minimo_y + maximo_y) / 2

        # Luego dibujamos los enlaces presentes
        for atomo1, conexiones in grafo.adyacencias.items():

            for atomo2 in conexiones:

                # Evitamos dibujar dos veces el mismo enlace
                if atomo1 < atomo2:

                    x1, y1 = posiciones[atomo1]
                    x2, y2 = posiciones[atomo2]

                    # Centramos respecto a la molécula
                    x1 -= centro_molecula_x
                    y1 -= centro_molecula_y

                    x2 -= centro_molecula_x
                    y2 -= centro_molecula_y

                    # Aplicamos la escala
                    x1 *= escala
                    y1 *= escala

                    x2 *= escala
                    y2 *= escala

                    # Colocamos la molécula en el centro
                    x1 += centro_x
                    y1 += centro_y

                    x2 += centro_x
                    y2 += centro_y

                    self.dibujar_enlace(
                        x1,
                        y1,
                        x2,
                        y2
                    )

        # Luego seguimos al dibujo delos atomos
        for identificador, (x, y) in posiciones.items():

            atomo = atomos_por_id[identificador]

            # Centramos respecto a la molécula
            x -= centro_molecula_x
            y -= centro_molecula_y

            # Aplicamos la escala
            x *= escala
            y *= escala

            # Colocamos la molécula en el centro
            x += centro_x
            y += centro_y

            self.dibujar_atomo(
                x,
                y,
                atomo.simbolo
            )