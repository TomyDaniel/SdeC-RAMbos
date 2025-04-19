# Python/gini_server32.py
import ctypes
import os
from msl.loadlib import Server32

# Asegúrate de que ctypes pueda encontrar la .so (ajusta la ruta si es necesario)
# Normalmente, si el servidor se inicia desde el directorio raíz, './libgini.so' funciona.
LIB_PATH = './libgini.so'
# Alternativamente, una ruta más robusta:
# LIB_PATH = os.path.join(os.path.dirname(__file__), '..', 'libgini.so')


class GiniServer32(Server32):
    """
    Servidor de 32 bits que carga libgini.so y expone sus funciones.
    """
    def __init__(self, host, port, **kwargs):
        # Carga la biblioteca libgini.so usando ctypes.CDLL
        # La ruta debe ser accesible desde donde se ejecute este servidor.
        super().__init__(LIB_PATH, 'cdll', host, port)

        # --- IMPORTANTE: Definir argtypes y restype AQUÍ ---
        # El servidor (32 bits) es quien interactúa directamente
        # con la biblioteca de 32 bits usando ctypes.

        # Accedemos a la biblioteca cargada a través de self.lib
        self.lib.sumar_uno.argtypes = [ctypes.c_float]
        self.lib.sumar_uno.restype = ctypes.c_float

        self.lib.promedio.argtypes = [ctypes.c_float, ctypes.c_float]
        self.lib.promedio.restype = ctypes.c_float

        self.lib.multiplicar.argtypes = [ctypes.c_float, ctypes.c_float]
        self.lib.multiplicar.restype = ctypes.c_float

        self.lib.dividir.argtypes = [ctypes.c_float, ctypes.c_float]
        self.lib.dividir.restype = ctypes.c_float

        # La función C se llama procesar_gini_final (que llama a la ASM)
        self.lib.procesar_gini_final.argtypes = [ctypes.c_float]
        self.lib.procesar_gini_final.restype = ctypes.c_int

        print(f"GiniServer32: Biblioteca {LIB_PATH} cargada. Funciones configuradas.")

    # --- Métodos que el cliente podrá llamar ---
    # Estos métodos simplemente llaman a las funciones correspondientes
    # de la biblioteca cargada (self.lib).

    def sumar_uno(self, valor):
        print(f"GiniServer32: Recibida llamada a sumar_uno({valor})")
        resultado = self.lib.sumar_uno(valor)
        print(f"GiniServer32: Devolviendo {resultado}")
        return resultado

    def promedio(self, a, b):
        print(f"GiniServer32: Recibida llamada a promedio({a}, {b})")
        resultado = self.lib.promedio(a, b)
        print(f"GiniServer32: Devolviendo {resultado}")
        return resultado

    def multiplicar(self, a, b):
        print(f"GiniServer32: Recibida llamada a multiplicar({a}, {b})")
        resultado = self.lib.multiplicar(a, b)
        print(f"GiniServer32: Devolviendo {resultado}")
        return resultado

    def dividir(self, a, b):
        print(f"GiniServer32: Recibida llamada a dividir({a}, {b})")
        if b == 0:
             # Manejar el error en el servidor es una opción
             raise ValueError("División por cero intentada en el servidor.")
        resultado = self.lib.dividir(a, b)
        print(f"GiniServer32: Devolviendo {resultado}")
        return resultado

    def procesar_gini_final(self, valor_gini):
        print(f"GiniServer32: Recibida llamada a procesar_gini_final({valor_gini})")
        resultado = self.lib.procesar_gini_final(valor_gini)
        print(f"GiniServer32: Devolviendo {resultado}")
        return resultado

# Nota: No necesitas ejecutar este script directamente.
# msl-loadlib lo ejecutará usando el intérprete de 32 bits cuando el cliente se conecte.