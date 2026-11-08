"""Ejercicio 2: un trabajador que no pierde mensajes aunque se caiga, y
que no reintenta para siempre un mensaje que nunca va a salir.

Corre las pruebas con:

    pytest test_trabajador_confiable_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from servicios import asunto_de_confirmacion


class TrabajadorConfiable:
    def __init__(self, cola, correo, cola_de_muertos, max_intentos):
        self.cola = cola
        self.correo = correo
        self.cola_de_muertos = cola_de_muertos
        self.max_intentos = max_intentos

    def procesar_uno(self):
        mensaje = self.cola.recibir()
        if mensaje is None:
            return False
 
        cuerpo = mensaje["cuerpo"]
        enviado = self.correo.enviar(cuerpo["estudiante"], asunto_de_confirmacion(cuerpo))
 
        if enviado:
            self.cola.confirmar(mensaje["id"])
        elif mensaje["intentos"] >= self.max_intentos:
            self.cola_de_muertos.publicar(cuerpo)
            self.cola.confirmar(mensaje["id"])
        
        return True

