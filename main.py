import tkinter as tk
from tkinter import ttk

from catalogo_compuestos import CATALOGO_COMPUESTOS
from analizador_formula import analizar_formula, crear_atomos, crear_lista_enlazada
from grafo import Grafo
from geometria import obtener_geometria
from representacion import Representacion

class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Convertidor de Estructuras Moleculares. Formula a Grafico")
        self.ventana.geometry("900x750")
        self.ventana.minsize(700,600)
        self.ventana.resizable(True, True)
        self.crear_interfaz()

    def crear_interfaz(self):

        # Contenedor principal del aplicacion
        self.frame_contenedor = tk.Frame(self.ventana)
        self.frame_contenedor.pack(
            fill="both",
            expand=True
        )

        # Canvas principal que nos permitirá desplazarnos
        self.canvas_principal = tk.Canvas(
            self.frame_contenedor,
            highlightthickness=0
        )

        # Barra de desplazamiento vertical
        self.scrollbar = ttk.Scrollbar(
            self.frame_contenedor,
            orient="vertical",
            command=self.canvas_principal.yview
        )

        self.canvas_principal.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas_principal.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Frame que contendrá toda la interfaz
        self.frame_principal = tk.Frame(
            self.canvas_principal
        )

        self.id_frame_principal = self.canvas_principal.create_window(
            (0, 0),
            window=self.frame_principal,
            anchor="nw"
        )

        # Actualizamos el área de desplazamiento
        self.frame_principal.bind(
            "<Configure>",
            lambda evento: self.canvas_principal.configure(
                scrollregion=self.canvas_principal.bbox("all")
            )
        )

        # Hacemos que el contenido ocupe todo el ancho disponible
        self.canvas_principal.bind(
            "<Configure>",
            lambda evento: self.canvas_principal.itemconfig(
                self.id_frame_principal,
                width=evento.width
            )
        )

        # Aqui ponemos el titulo
        titulo = tk.Label(
            self.frame_principal,
            text="Estructuras Moleculares",
            font=("Arial", 18, "bold")
        )

        titulo.pack(
            pady=(30, 10)
        )

        #Despues colo camos un subtitulo
        subtitulo = tk.Label(
            self.frame_principal,
            text="Convierte formula molecular en una representación gráfica",
            font=("Arial", 11)
        )

        subtitulo.pack(
            pady=(0, 10)
        )

        #Procedemos a colocar un select
        etiqueta_compuesto = tk.Label(
            self.frame_principal,
            text="Selecciona un compuesto",
            font=("Arial", 12)
        )

        etiqueta_compuesto.pack()

        self.comp_sel = tk.StringVar()

        self.lista_compuestos = ttk.Combobox(
            self.frame_principal,
            textvariable=self.comp_sel,
            state="readonly",
            width=50,
            font=("Arial", 11)
        )

        self.lista_compuestos["values"] = list(
            CATALOGO_COMPUESTOS.keys()
        )

        self.lista_compuestos.pack(
            pady=10
        )

        self.lista_compuestos.bind(
            "<<ComboboxSelected>>",
            self.mostrar_compuesto
        )

        #Mostramos la infoemacion del compuesto
        self.frame_formula = tk.Frame(
            self.frame_principal
        )

        self.label_nombre = tk.Label(
            self.frame_formula,
            text="",
            font=("Arial", 16, "bold")
        )

        self.label_nombre.pack(
            pady=(20, 5)
        )

        self.label_formula = tk.Label(
            self.frame_formula,
            text="",
            font=("Arial", 28, "bold")
        )

        self.label_formula.pack(
            pady=5
        )

        # Mostramos un mensaje con la instruccion
        self.label_instruccion = tk.Label(
            self.frame_formula,
            text="Escribe la formula que te mostramos arriba",
            font=("Arial", 11)
        )

        self.label_instruccion.pack(
            pady=(20, 5)
        )

        # Input encargado de obtener el dato ingresado por el usuario
        self.entrada_formula = tk.Entry(
            self.frame_formula,
            font=("Arial", 16),
            justify="center",
            width=20
        )

        self.entrada_formula.pack(
            pady=5
        )

        # Boton para ejecutar las funciones
        self.boton_visualizar = tk.Button(
            self.frame_formula,
            text="Visualizar",
            font=("Arial", 11, "bold"),
            width=18,
            state="disabled",
            command=self.visualizar
        )

        self.boton_visualizar.pack(
            pady=20
        )

        # Area para mostrar resultados
        self.label_mensaje = tk.Label(
            self.frame_formula,
            text="",
            font=("Arial", 11)
        )

        self.label_mensaje.pack(
            pady=5
        )

        self.frame_resultado = tk.Frame(
            self.frame_formula
        )

        self.label_resultado = tk.Label(
            self.frame_resultado,
            text="",
            font=("Arial", 11),
            justify="left",
            anchor="w"
        )

        self.label_resultado.pack(
            pady=10
        )

        # Area donde se mostrará el dibujo de la molecula
        self.canvas_molecula = tk.Canvas(
            self.frame_resultado,
            width=600,
            height=600,
            bg="white"
        )

        self.representacion = Representacion(
            self.canvas_molecula
        )

    #PROCESO CON COMPESTO SELECCIONADO
    #Funcion mostrar el compuesto seleccionado
    def mostrar_compuesto(self, evento=None):
        nombre = self.comp_sel.get()
        datos = CATALOGO_COMPUESTOS[nombre]

        self.label_nombre.config(text=nombre)
        self.label_formula.config(
            text=self.convertir_subindices(datos["formula"])
        )
        self.frame_formula.pack()
        self.entrada_formula.delete(0, tk.END)
        self.label_mensaje.config(text="")
        self.boton_visualizar.config(state="normal")
        self.entrada_formula.focus()

    #Funcion visualizar
    def visualizar(self):
        #Corroboramos que la formula este bien escrita
        nombre = self.comp_sel.get()
        datos = CATALOGO_COMPUESTOS[nombre]
        formula_correcta = datos["formula"]
        formula_usuario = self.entrada_formula.get().strip()
        if formula_usuario.upper() == formula_correcta.upper():
            self.label_mensaje.config(
                text="✓ Formula correcta",
                fg="green"
            )
            resultado = analizar_formula(formula_correcta)
            atomos = crear_atomos(resultado)

            lista = crear_lista_enlazada(atomos)

            grafo = Grafo()
            grafo.agregar_atomos(atomos)

            conexiones = datos["conexiones"]
            grafo.agregar_conexiones(atomos, conexiones)

            enlaces = grafo.cantidad_enlaces()

            geometria = obtener_geometria(datos)

            #Aqui contemplamos el tipo de gometria y decidimos que funion usar para dibujar la molecula
            if geometria.tipo == "Lineal":
                posiciones = geometria.generar_posiciones_lineales(grafo)

            elif geometria.tipo == "Angular":
                posiciones = geometria.generar_posiciones_angulares(grafo)

            elif geometria.tipo == "Trigonal plana":
                posiciones = geometria.generar_posiciones_trigonal_plana(grafo)

            elif geometria.tipo == "Trigonal piramidal":
                posiciones = geometria.generar_posiciones_trigonal_piramidal(grafo)

            elif geometria.tipo == "Tetraédrica" and len(atomos) <= 5:
                posiciones = geometria.generar_posiciones_tetraedrica(grafo)

            elif geometria.tipo == "Octaédrica":
                posiciones = geometria.generar_posiciones_octaedrica(grafo)

            elif len(atomos) > 5:
                posiciones = geometria.generar_posiciones_molecula(
                    grafo,
                    atomos
                )

            else:
                posiciones = {}


            #Mostramos la informacion de texto
            self.label_resultado.config(
                text = (
                    f"Compuesto: {nombre}\n"
                    f"Formula: {formula_correcta}\n"
                    f"Atomos: {lista.cantidad()}\n"
                    f"Enlaces: {enlaces}\n"
                    f"Geometria: {geometria.tipo}\n"
                    f"Angulo: {geometria.angulo}\n"
                )
            )
            self.frame_resultado.pack()
            self.canvas_molecula.pack(pady=10)
            self.representacion.dibujar_molecula(
                atomos,
                grafo,
                posiciones,
                centro_x=300,
                centro_y=300
            )
            print("Formula correcta")
            print("Atomos: ", lista.cantidad())
            print("Enlaces: ", enlaces)
            print("Geometria: ", geometria.tipo)
            print("Angulo: ", geometria.angulo)

        else:
            self.label_mensaje.config(
                text="⚠ La formula no coincide. Intentalo de nuevo",
                fg="red"
            )
            print("Formula incorrecta")

    def convertir_subindices(self, formula):
        tabla = str.maketrans("0123456789","₀₁₂₃₄₅₆₇₈₉")
        return formula.translate(tabla)

# Inicializacion de la aplicacion
ventana = tk.Tk()
app = Aplicacion(ventana)
ventana.mainloop()















