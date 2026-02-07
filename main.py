import tkinter as tk
from interfaz import AplicacionHabilidades

if __name__ == "__main__":
    # ventana principal
    raiz_ventana = tk.Tk()
    
    # se instancia la interfaz
    app = AplicacionHabilidades(raiz_ventana)
    
    # bucle de eventos
    raiz_ventana.mainloop()