class NodoHabilidad:
    """Estructura para los nodos en los Árboles Binarios"""
    def __init__(self, id, nombre, costo):
        self.id = id
        self.nombre = nombre
        self.costo = costo
        self.desbloqueado = False
        self.izquierdo = None
        self.derecho = None
        self.padre = None  
        self.prerrequisitos_cruzados = []