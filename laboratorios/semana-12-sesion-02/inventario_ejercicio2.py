"""Ejercicio 2: espacios y equipos en el mismo arbol.

La expansion de ReservaU incluye el prestamo de equipos: proyectores en
la biblioteca y balones en el complejo deportivo. Un proyector se reserva
igual que una sala, por franjas, asi que es un Reservable mas, con su tipo.

Recurso tiene ahora cuatro operaciones, y las dos clases del arbol
(Reservable, la hoja, y Grupo, el compuesto) las implementan:

- buscar(tipo, inicio, fin): los nombres de los reservables de ese tipo
  libres en esa franja, en el orden del arbol.
- contar(tipo): cuantos reservables de ese tipo hay.
- encontrar(nombre): el reservable con ese nombre, o None si no esta.
- rutas(tipo, inicio, fin, ruta): como buscar, pero cada nombre con la
  ruta desde el nodo donde se empezo a buscar, separada por " / ":
  "Campus Cumbaya / Biblioteca / Prestamos / proyector-1". Quien llama
  desde arriba pasa ruta = "".

reservar_en(raiz, nombre, ...) ya esta escrita: encuentra el reservable
por su nombre y lo reserva. No sabe en que nivel esta.

Corre el archivo con:

    python3 inventario_ejercicio2.py

y las pruebas con:

    pytest test_inventario_ejercicio2.py
"""

from reservas import CalendarioDeCancha

FECHA = "2026-11-10"


class Recurso:
    def __init__(self, nombre):
        self.nombre = nombre

    def buscar(self, tipo, inicio, fin):
        raise NotImplementedError

    def contar(self, tipo):
        raise NotImplementedError

    def encontrar(self, nombre):
        raise NotImplementedError

    def rutas(self, tipo, inicio, fin, ruta):
        resultado = []
        for hijo in self.hijos:
            resultado = resultado + hijo.rutas(tipo, inicio, fin, ruta + self.nombre + " / ")
        return resultado


class Reservable(Recurso):
    def __init__(self, nombre, tipo):
        super().__init__(nombre)
        self.tipo = tipo
        self.calendario = CalendarioDeCancha(nombre, FECHA)

    def reservar(self, id_reserva, estudiante, inicio, fin):
        self.calendario.reservar(id_reserva, estudiante, inicio, fin)

    def buscar(self, tipo, inicio, fin):
        if self.tipo == tipo and self.calendario.esta_libre(inicio, fin):
            return [self.nombre]
        return []

    def contar(self, tipo):
        if self.tipo == tipo:
            return 1
        return 0


    def encontrar(self, nombre):
        if self.nombre == nombre:
            return self
        return None

    def rutas(self, tipo, inicio, fin, ruta):
        if len(self.buscar(tipo, inicio, fin)) > 0:
            return [ruta + self.nombre]
        return []


class Grupo(Recurso):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.hijos = []

    def agregar(self, hijo):
        self.hijos.append(hijo)

    def buscar(self, tipo, inicio, fin):
        resutlado = []
        for hijo in self.hijos:
            resutlado = resutlado + hijo.buscar(tipo, inicio, fin)
        return resutlado

    def contar(self, tipo):
        total = 0
        for hijo in self.hijos:
            total = total + hijo.contar(tipo)
        return total

    def encontrar(self, nombre):
        for hijo in self.hijos:
            encontrado = hijo.encontrar(nombre)
            if encontrado is not None:
                return encontrado
        return None     

    def ruta(self, tipo, inicio, fin, ruta):
        resultado = []
        for hijo in self.hijos:
            resultado = resultado + hijo.rutas(tipo, inicio, fin, ruta)
        return resultado

def reservar_en(raiz, nombre, id_reserva, estudiante, inicio, fin):
    reservable = raiz.encontrar(nombre)
    if reservable is None:
        raise ValueError("recurso desconocido")
    reservable.reservar(id_reserva, estudiante, inicio, fin)


def armar_campus():
    complejo = Grupo("Complejo deportivo")
    complejo.agregar(Reservable("cancha-1", "cancha"))
    complejo.agregar(Reservable("cancha-2", "cancha"))
    bodega = Grupo("Bodega")
    bodega.agregar(Reservable("balon-1", "balon"))
    bodega.agregar(Reservable("balon-2", "balon"))
    complejo.agregar(bodega)

    piso_1 = Grupo("Piso 1")
    piso_1.agregar(Reservable("sala-101", "sala"))
    piso_1.agregar(Reservable("sala-102", "sala"))
    prestamos = Grupo("Prestamos")
    prestamos.agregar(Reservable("proyector-1", "proyector"))
    prestamos.agregar(Reservable("proyector-2", "proyector"))
    biblioteca = Grupo("Biblioteca")
    biblioteca.agregar(piso_1)
    biblioteca.agregar(prestamos)

    campus = Grupo("Campus Cumbaya")
    campus.agregar(complejo)
    campus.agregar(biblioteca)
    return campus


if __name__ == "__main__":
    campus = armar_campus()
    reservar_en(campus, "proyector-1", "r-1", "ana", 18, 19)
    reservar_en(campus, "sala-101", "r-2", "beto", 18, 19)
    print("Proyectores libres de 18 a 19:", campus.buscar("proyector", 18, 19))
    print("Salas libres de 18 a 19:", campus.buscar("sala", 18, 19))
    print("Balones en el campus:", campus.contar("balon"))
    print("Donde hay un balon libre de 18 a 19:")
    for ruta in campus.rutas("balon", 18, 19, ""):
        print(" ", ruta)
    print("No existe:", campus.encontrar("proyector-9"))
