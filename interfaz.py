import tkinter as tk
from tkinter import messagebox
from logica import SistemaHabilidades
class AplicacionHabilidades:
    """Interfaz del programa :]"""
    
    def __init__(self, ventana):
        # ventana principal
        self.ventana = ventana
        self.ventana.title("SISTEMA DE HABILIDADES - ÁRBOL & GRAFO")
        self.ventana.geometry("1100x900")
        self.ventana.configure(bg="#0b0d17") # Fondo azul oscuro profundo
        
        # controlador de la parte logica
        self.sistema = SistemaHabilidades()
        
        # TODOS LOS DEMAS COMPONENTES :]
        
        # muestra los puntos actualizados
        self.etiqueta_puntos = tk.Label(ventana, text="", font=("Fixedsys", 22, "bold"), 
                                        bg="#0b0d17", fg="#00ffcc")
        self.etiqueta_puntos.pack(pady=15)

        # lienzo de los arboles
        self.lienzo = tk.Canvas(ventana, bg="#0d1117", width=1050, height=600, 
                               highlightthickness=1, highlightbackground="#00ffcc")
        self.lienzo.pack()
        
        # botón de reinicio
        tk.Button(ventana, text="REINICIAR PROGRESO", command=self.ejecutar_reinicio, 
                  bg="#c0392b", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
        
        # cuadro con la guía de la guía de las dependencias de los grafos
        tk.Label(ventana, text="GUÍA DE COMBINACIONES", bg="#0b0d17", fg="cyan", 
                 font=("Arial", 10, "bold")).pack()
        
        # cuadro de texto informativo para dependencias que no son líneas en el árbol
        self.txt_guia = tk.Text(ventana, height=4, width=80, bg="#161b22", fg="#8b949e", 
                                font=("Consolas", 10))
        self.txt_guia.insert("1.0", "• [Explosión] requiere [Atk Pesado]\n"
                                    "• [Reflejo] requiere [Mana]\n"
                                    "• [Congelar] requiere [Escudo]")
        self.txt_guia.config(state="disabled") # solo para lectura
        self.txt_guia.pack(pady=5)
        self.crear_cuadro_integrantes()
        # Dibujar los arboles iniciales
        self.actualizar_interfaz()

    def crear_cuadro_integrantes(self):
        """Crea un cuadro flotante en la esquina inferior derecha para los autores"""
        # Marco contenedor posicionado en la esquina (South-East)
        self.marco_equipo = tk.Frame(self.ventana, bg="#0b0d17", padx=10, pady=10)
        self.marco_equipo.place(relx=1.0, rely=1.0, anchor="se")

        # Título del equipo
        tk.Label(self.marco_equipo, text="Integrantes:", bg="#0b0d17", fg="cyan", 
                 font=("Arial", 9, "bold")).pack(anchor="e")

        # Lista de nombres
        integrantes = (
            "Antoni Cortez. 31412808\n"
            "Alexander Cova\n"
            "Betania Campos. 26975684\n"
            "Bramdon Fuentes. 30079515\n"
            "Claudia Suárez\n"
            "Julio Cabello"
        )

        # Etiqueta con los nombres alineados a la derecha
        tk.Label(self.marco_equipo, text=integrantes, bg="#0b0d17", fg="#08eb5f", 
                 font=("Consolas", 8), justify="right").pack(anchor="e")    
    def dibujar_rama(self, nodo, x, y, sep_h):
        """Función recursiva para renderizar el Árbol Binario"""
        if not nodo: return
        
        dist_v = 110 # Distancia vertical fija entre los niveles del árbol
        
        # CONEXIONES DE LOS ARBOLES
        if nodo.izquierdo:
            xh, yh = x - sep_h, y + dist_v
            self.lienzo.create_line(x, y, xh, yh, fill="#00ffff", width=3)
            # Llamada para el hijo izquierdo 
            self.dibujar_rama(nodo.izquierdo, xh, yh, sep_h * 0.55)
            
        if nodo.derecho:
            xh, yh = x + sep_h, y + dist_v
            self.lienzo.create_line(x, y, xh, yh, fill="#00ffff", width=3)
            # Llamada  para el hijo derecho
            self.dibujar_rama(nodo.derecho, xh, yh, sep_h * 0.55)

        # LÓGICA VISUAL DE COLORES 
        if nodo.desbloqueado:
            color = "#238636" # Habilidad ya comprada
        elif nodo.padre and not nodo.padre.desbloqueado:
            color = "#21262d" # Bloqueada por jerarquía de arbol (falta el padre)
        else:
            color = "#8b1111" # Disponible para comprar (cumple requisitos)
        
        # Para dibujar el nodo como círculo
        circ = self.lienzo.create_oval(x-35, y-35, x+35, y+35, fill=color, 
                                      outline="white", width=2)
        
        # Para escribir el nombre y costo dentro del círculo
        self.lienzo.create_text(x, y, text=f"{nodo.nombre}\n{nodo.costo} PT", 
                                fill="white", font=("Arial", 8, "bold"), justify="center")
        
        # Vincular el clic del ratón con la compra
        self.lienzo.tag_bind(circ, "<Button-1>", lambda e, id_h=nodo.id: self.intentar_compra(id_h))

    def intentar_compra(self, id_h):
        """Maneja la interacción de clic: pregunta a la lógica si se puede desbloquear"""
        puede, msg = self.sistema.se_puede_desbloquear(id_h)
        
        if puede:
            # Marca como desbloqueado y se cobran puntos
            h = self.sistema.todas_las_habilidades[id_h]
            h.desbloqueado = True
            self.sistema.puntos -= h.costo
            self.actualizar_interfaz() # Muestra los cambios
        else:
            # Muestra mensaje de error
            messagebox.showwarning("Bloqueado", msg)

    def ejecutar_reinicio(self):
        """Resetea el sistema completo tras confirmación del usuario"""
        if messagebox.askyesno("Confirmar", "¿Deseas reiniciar todo el progreso?"):
            self.sistema.reiniciar_todo()
            self.actualizar_interfaz()

    def actualizar_interfaz(self):
        """Limpia y redibuja toda la pantalla para reflejar el estado actual"""
        self.etiqueta_puntos.config(text=f"PUNTOS DE PODER: {self.sistema.puntos}")
        self.lienzo.delete("all") # Borrar dibujos anteriores
        
        # Cuadrícula de fondo
        for i in range(0, 1050, 50): self.lienzo.create_line(i, 0, i, 600, fill="#121821")
        for j in range(0, 600, 50): self.lienzo.create_line(0, j, 1100, j, fill="#121821")
        
        # Iniciar el dibujo recursivo desde las dos raíces (Bosque de Árboles)
        self.dibujar_rama(self.sistema.raices["Combate"], 270, 70, 150)

        self.dibujar_rama(self.sistema.raices["Magia"], 780, 70, 150)

