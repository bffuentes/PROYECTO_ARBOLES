# logica.py
from modelos import NodoHabilidad

class SistemaHabilidades:
    def __init__(self):
        self.puntos_iniciales = 50
        self.puntos = self.puntos_iniciales
        self.raices = {"Combate": None, "Magia": None}
        self.todas_las_habilidades = {}
        self._inicializar_datos() #valores iniciales para las variables principales

    def _inicializar_datos(self):
        # ARBOL DE COMBATE
        raiz_c = NodoHabilidad("c_base", "Espada", 2)
        raiz_c.izquierdo = NodoHabilidad("c_escudo", "Escudo", 3)
        raiz_c.izquierdo.izquierdo = NodoHabilidad("c_bloqueo", "Bloqueo", 4)
        raiz_c.izquierdo.derecho = NodoHabilidad("c_reflejo", "Reflejo", 4)
        raiz_c.derecho = NodoHabilidad("c_pesado", "Atk Pesado", 3)
        raiz_c.derecho.izquierdo = NodoHabilidad("c_torbe", "Torbellino", 5)

        # ARBOL DE MAGIA
        raiz_m = NodoHabilidad("m_base", "Mana", 2)
        raiz_m.izquierdo = NodoHabilidad("m_fuego", "Fuego", 4)
        raiz_m.izquierdo.derecho = NodoHabilidad("m_explo", "Explosión", 5)
        raiz_m.derecho = NodoHabilidad("m_hielo", "Hielo", 4)
        raiz_m.derecho.izquierdo = NodoHabilidad("m_venti", "Ventisca", 5)
        raiz_m.derecho.derecho = NodoHabilidad("m_conge", "Congelar", 5)

        self.raices["Combate"] = raiz_c
        self.raices["Magia"] = raiz_m
        
        for r in self.raices.values():
            self._mapear_recursivo(r)

        # GRAFO: Dependencias cruzadas
        self.todas_las_habilidades["m_explo"].prerrequisitos_cruzados.append("c_pesado")
        self.todas_las_habilidades["c_reflejo"].prerrequisitos_cruzados.append("m_base")
        self.todas_las_habilidades["m_conge"].prerrequisitos_cruzados.append("c_escudo")

    def _mapear_recursivo(self, nodo, padre_actual=None):
        if nodo:
            nodo.padre = padre_actual  
            self.todas_las_habilidades[nodo.id] = nodo
            self._mapear_recursivo(nodo.izquierdo, nodo)
            self._mapear_recursivo(nodo.derecho, nodo)

    def se_puede_desbloquear(self, id_h):
        h = self.todas_las_habilidades[id_h]
        if h.desbloqueado: return False, "Ya la conoces."
        if self.puntos < h.costo: return False, "Puntos insuficientes."
        
        # Árbol: Validar padre
        if h.padre and not h.padre.desbloqueado:
            return False, f"Bloqueado: Requiere {h.padre.nombre}"
        
        # Grafo: Validar externos
        for id_pre in h.prerrequisitos_cruzados:
            if not self.todas_las_habilidades[id_pre].desbloqueado:
                return False, "Necesitas habilidad externa"
        return True, "Disponible"

    def reiniciar_todo(self):
        self.puntos = self.puntos_iniciales
        for h in self.todas_las_habilidades.values():
            h.desbloqueado = False