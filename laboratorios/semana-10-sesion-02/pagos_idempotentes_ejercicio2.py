"""Ejercicio 2: el pago de la garantia, idempotente con una cabecera
Idempotency-Key.

Corre las pruebas con:

    pytest test_pagos_idempotentes_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from http_simulado import Respuesta


class ApiDePagos:
    def __init__(self, repositorio, pasarela):
        self.repositorio = repositorio
        self.pasarela = pasarela
        self.respuestas_guardadas = {}

    def manejar(self, solicitud):
        if solicitud.metodo == "POST" and solicitud.ruta == "/v1/pagos":
            return self.crear_pago(solicitud)
        return Respuesta(404, {"error": "ruta desconocida"})

    def crear_pago(self, solicitud):
        clave = solicitud.cabeceras.get("Idempotency-Key")
        if clave is None:
            return Respuesta(400, {"error": "falta Idempotency-Key"})
 
        cuerpo = solicitud.cuerpo
        if clave in self.respuestas_guardadas:
            guardado = self.respuestas_guardadas[clave]
            if guardado["cuerpo"] == cuerpo:
                return guardado["respuesta"]
            return Respuesta(422, {"error": "clave usada con otro cuerpo"})
 
        reserva = self.repositorio.buscar(cuerpo["reserva_id"])
        if reserva is None:
            return Respuesta(404, {"error": "reserva desconocida"})
 
        id_cobro = self.pasarela.cobrar(reserva["estudiante"], cuerpo["monto"])
        respuesta = Respuesta(201, {"id": id_cobro, "reserva_id": cuerpo["reserva_id"], "monto": cuerpo["monto"]})
        self.respuestas_guardadas[clave] = {"cuerpo": dict(cuerpo), "respuesta": respuesta}
        return respuesta