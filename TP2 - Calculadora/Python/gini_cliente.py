# Python/gini_cliente.py

# Quitar la importación directa de ctypes para cargar la lib
# import ctypes
# PERO MANTENERLA si necesitas los tipos c_float, c_int para pasar a la API
# (aunque msl-loadlib suele manejar bien los tipos nativos de Python)
# Por seguridad o claridad, puedes mantenerla:
import ctypes # Necesario si usas c_float explícitamente abajo

# Usar msl-loadlib para el cliente
from msl.loadlib import Client64

# Tus otras importaciones
from API import obtener_gini
import datetime
import sys # Para manejo de errores

# --- Clase Cliente (64 bits) ---
class GiniClient64(Client64):
    """
    Cliente de 64 bits que se comunica con GiniServer32.
    """
    def __init__(self):
        # Especifica el nombre del MÓDULO Python que contiene la clase Server32
        # msl-loadlib buscará Python/gini_server32.py
        super().__init__(module32='Python.gini_server') # Usa notación de punto para el módulo

        print("GiniClient64: Conectado al servidor de 32 bits.")

    # --- Métodos que llaman al servidor usando request32 ---
    # Nota: No definimos argtypes/restype aquí. Eso lo hace el servidor.

    def sumar_uno(self, valor):
        # Llama al método 'sumar_uno' en el GiniServer32
        return self.request32('sumar_uno', valor)

    def promedio(self, a, b):
        return self.request32('promedio', a, b)

    def multiplicar(self, a, b):
        return self.request32('multiplicar', a, b)

    def dividir(self, a, b):
         # La validación de b!=0 puede hacerse aquí o en el servidor
        if b == 0:
            print("⚠️ Cliente: No se puede dividir por cero.")
            return None # O lanzar una excepción local
        try:
            return self.request32('dividir', a, b)
        except Exception as e: # Captura errores del servidor
            print(f"Error del servidor en división: {e}")
            return None


    def procesar_gini_final(self, valor_gini):
        # Asegúrate de pasar un float, ya que el servidor espera c_float
        # Puedes usar ctypes.c_float si quieres ser explícito, o pasar un float Python
        # gini_float_arg = ctypes.c_float(valor_gini) # Opción explícita
        # return self.request32('procesar_gini_final', gini_float_arg)
        return self.request32('procesar_gini_final', float(valor_gini)) # Pasar float estándar


# --- Tu código existente ---

def guardar_resultado(operacion, original, resultado):
    # (Sin cambios)
    with open("resultados_gini.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - Operación: {operacion}, GINI original: {original}, Resultado: {resultado}\n")

# Menú interactivo
def menu(client): # Pasamos el objeto cliente
    while True:
        print("\n--- Calculadora GINI en ASM (via msl-loadlib) ---")
        print("1. Sumar 1")
        print("2. Promedio")
        print("3. Multiplicación")
        print("4. División")
        print("5. Obtener Gini de un país y procesar (+1)")
        print("0. Salir")
        opcion = input("Seleccioná una opción: ")

        try: # Añadir manejo de errores para llamadas al cliente
            if opcion == "1":
                val = float(input("Ingresá el valor: "))
                resultado = client.sumar_uno(val) # Usar el cliente
                print(f"Resultado: {resultado}")
                guardar_resultado("sumar_uno", val, resultado)

            elif opcion == "2":
                a = float(input("Primer número: "))
                b = float(input("Segundo número: "))
                resultado = client.promedio(a, b) # Usar el cliente
                print(f"Promedio: {resultado}")
                guardar_resultado("promedio", f"{a}, {b}", resultado)

            elif opcion == "3":
                a = float(input("Primer número: "))
                b = float(input("Segundo número: "))
                resultado = client.multiplicar(a, b) # Usar el cliente
                print(f"Multiplicación: {resultado}")
                guardar_resultado("multiplicar", f"{a}, {b}", resultado)

            elif opcion == "4":
                a = float(input("Dividendo: "))
                b = float(input("Divisor: "))
                resultado = client.dividir(a, b) # Usar el cliente
                if resultado is not None: # Chequear si hubo error (devuelve None en caso de div/0)
                    print(f"División: {resultado}")
                    guardar_resultado("dividir", f"{a}, {b}", resultado)
                # Si es None, el cliente ya imprimió el mensaje de error

            elif opcion == "5":
                pais = input("Ingresá el código del país (ej: ARG, BRA, MEX): ").upper()
                gini_valor = obtener_gini(pais)
                if gini_valor is not None:
                    print(f"Gini original desde API ({pais}): {gini_valor}")
                    # Llamar a la función del cliente
                    resultado_int = client.procesar_gini_final(gini_valor)
                    print(f"Gini (entero) + 1 con ASM: {resultado_int}")
                    guardar_resultado(f"API + procesar_gini_final ({pais})", gini_valor, resultado_int)
                else:
                    print(f"No se pudo obtener GINI para {pais}.")

            elif opcion == "0":
                print("Cerrando cliente y servidor...")
                # Al salir del scope o cerrar el programa, msl-loadlib debería
                # intentar cerrar el servidor, pero es bueno hacerlo explícito si hay un método.
                # En este caso, la simple salida del programa debería bastar.
                print("¡Hasta luego!")
                break

            else:
                print("Opción inválida. Intentá de nuevo.")

        except Exception as e:
            print(f"\n--- ERROR INESPERADO ---")
            print(f"Ocurrió un error: {e}")
            print("Puede que el servidor de 32 bits haya fallado.")
            # Considera añadir lógica para intentar reconectar o salir.


# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    print("Iniciando cliente GINI (64 bits)...")
    # Asegúrate de tener instalado python3:i386 y msl-loadlib
    # pip install msl-loadlib

    try:
        # Crear una instancia del cliente
        gini_client = GiniClient64()

        # Ejecutar el menú pasándole el cliente
        menu(gini_client)

    except FileNotFoundError:
         print("\n--- ERROR CRÍTICO ---")
         print("No se encontró 'libgini.so'. Asegúrate de que esté compilada y en el directorio raíz.")
         print("Ejecuta 'make' para compilarla.")
         sys.exit(1)
    except Exception as e:
        # Captura errores durante la inicialización del cliente/servidor
        print("\n--- ERROR CRÍTICO AL INICIAR ---")
        print(f"No se pudo iniciar la comunicación con el servidor 32 bits: {e}")
        print("Verifica:")
        print("  1. ¿Está instalado 'python3:i386'?")
        print("  2. ¿Está instalada la biblioteca 'msl-loadlib' (`pip install msl-loadlib`)?")
        print("  3. ¿Hay algún problema con la biblioteca './libgini.so' o sus dependencias de 32 bits?")
        sys.exit(1)