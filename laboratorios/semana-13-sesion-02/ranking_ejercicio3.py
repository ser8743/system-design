"""Ejercicio 3: el orden del feed y los espacios mas reservados.

Mostrar el feed de lo mas nuevo a lo mas viejo es justo y es aburrido: un
entrenamiento de hace 5 minutos tapa el partido de tu propio equipo, que
ya tiene 40 confirmaciones. ReservaU pide un ranking simple, que se pueda
explicar en una oracion.

OrdenadorDeFeed se construye con dos diccionarios:
- interacciones: id de publicacion -> cuantas personas confirmaron
  asistencia o comentaron (0 si no aparece).
- equipos_de: estudiante -> lista de autores (equipos) en los que juega
  (lista vacia si no aparece).

Metodos:

- puntaje(publicacion, estudiante, ahora): (interacciones + 1) multiplicado
  por 3 si el autor es un equipo del estudiante (por 1 si no), dividido
  para (1 + horas), donde horas es (ahora - publicacion.momento) // 60
  (los momentos estan en minutos).

- ordenar(publicaciones, estudiante, ahora, cantidad): las `cantidad`
  publicaciones de mayor puntaje. En un empate de puntaje, primero la mas
  nueva (mayor momento), y si tambien empatan, la de id menor. Ademas,
  nunca tres seguidas del mismo autor: si la siguiente por puntaje seria
  la tercera seguida de ese autor, va la mejor de otro autor; si no queda
  ninguna de otro autor, va igual.

- espacios_mas_reservados(reservas, ahora, cantidad): reservas es una lista
  de tuplas (espacio, momento). Cuenta, por espacio, las reservas con
  momento en los ultimos 7 dias (ahora - 10080 < momento <= ahora), y
  devuelve una lista de tuplas (espacio, conteo) con los `cantidad` de
  mayor conteo; en un empate, primero el nombre menor. Los espacios sin
  reservas en esa ventana no aparecen.

Esta vez no hay codigo de partida. Corre las pruebas con:

    pytest test_ranking_ejercicio3.py
"""


from actividad import Publicacion

class OrdenadorDeFeed:
    def __init__(self, interacciones, equipos_de):
        self.interacciones = interacciones
        self.equipos_de = equipos_de

    def puntaje(self, publicacion, estudiante, ahora):
        confirmaciones = self.interacciones.get(publicacion.id, 0)
        if publicacion.autor in self.equipos_de.get(estudiante, []):
            factor = 3
        else:
            factor = 1
        horas = (ahora - publicacion.momento) // 60
        return (confirmaciones + 1) * factor / (1 + horas)

    def la_mejor(self, candidatas, estudiante, ahora):
        mejor = candidatas[0]
        mejor_puntaje = self.puntaje(mejor, estudiante, ahora)
        for otra in candidatas[1:]:
            puntaje = self.puntaje(otra, estudiante, ahora)
            if puntaje > mejor_puntaje:
                mejor = otra
                mejor_puntaje = puntaje
            elif puntaje == mejor_puntaje:
                if otra.momento > mejor.momento:
                    mejor = otra
                elif otra.momento == mejor.momento and otra.id < mejor.id:
                    mejor = otra
        return mejor

    def ordenar(self, publicaciones, estudiante, ahora, cantidad):
        resultado = []
        restantes = publicaciones[:]
        while len(resultado) < cantidad and len(restantes) > 0:
            autor_vetado = None
            if len(resultado) >= 2 and resultado[-1].autor == resultado[-2].autor:
                autor_vetado = resultado[-1].autor

            permitidas = []
            for publicacion in restantes:
                if publicacion.autor != autor_vetado:
                    permitidas.append(publicacion)
            if len(permitidas) == 0:
                permitidas = restantes

            elegida = self.la_mejor(permitidas, estudiante, ahora)
            resultado.append(elegida)
            restantes.remove(elegida)
        return resultado

    def espacios_mas_reservados(self, reservas, ahora, cantidad):
        conteos = {}
        for reserva in reservas:
            espacio = reserva[0]
            momento = reserva[1]
            if ahora - 10080 < momento <= ahora:
                if espacio not in conteos:
                    conteos[espacio] = 0
                conteos[espacio] = conteos[espacio] + 1

        pendientes = []
        for espacio in conteos:
            pendientes.append((espacio, conteos[espacio]))

        resultado = []
        while len(resultado) < cantidad and len(pendientes) > 0:
            mejor = pendientes[0]
            for otro in pendientes[1:]:
                if otro[1] > mejor[1]:
                    mejor = otro
                elif otro[1] == mejor[1] and otro[0] < mejor[0]:
                    mejor = otro
            resultado.append(mejor)
            pendientes.remove(mejor)
        return resultado
