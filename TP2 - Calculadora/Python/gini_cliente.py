import ctypes
from API import obtener_gini
import datetime

# Cargar la biblioteca compartida
lib = ctypes.CDLL('./libgini.so')

# Configurar las funciones
lib.sumar_uno.argtypes = [ctypes.c_float]
lib.sumar_uno.restype = ctypes.c_float

lib.promedio.argtypes = [ctypes.c_float, ctypes.c_float]
lib.promedio.restype = ctypes.c_float

lib.multiplicar.argtypes = [ctypes.c_float, ctypes.c_float]
lib.multiplicar.restype = ctypes.c_float

lib.dividir.argtypes = [ctypes.c_float, ctypes.c_float]
lib.dividir.restype = ctypes.c_float

def guardar_resultado(operacion, original, resultado):
    with open("resultados_gini.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - Operación: {operacion}, GINI original: {original}, Resultado: {resultado}\n")

# Menú interactivo
def menu():
    while True:
        print("\n--- Calculadora GINI en ASM ---")
        print("1. Sumar 1")
        print("2. Promedio")
        print("3. Multiplicación")
        print("4. División")
        print("5. Obtener Gini de un país")
        print("0. Salir")
        opcion = input("Seleccioná una opción: ")

        if opcion == "1":
            val = float(input("Ingresá el valor: "))
            resultado = lib.sumar_uno(val)
            print(f"Resultado: {resultado}")
            guardar_resultado("sumar_uno", val, resultado)

        elif opcion == "2":
            a = float(input("Primer número: "))
            b = float(input("Segundo número: "))
            resultado = lib.promedio(a, b)
            print(f"Promedio: {resultado}")
            guardar_resultado("promedio", f"{a}, {b}", resultado)

        elif opcion == "3":
            a = float(input("Primer número: "))
            b = float(input("Segundo número: "))
            resultado = lib.multiplicar(a, b)
            print(f"Multiplicación: {resultado}")
            guardar_resultado("multiplicar", f"{a}, {b}", resultado)

        elif opcion == "4":
            a = float(input("Dividendo: "))
            b = float(input("Divisor: "))
            if b == 0:
                print("⚠️ No se puede dividir por cero.")
            else:
                resultado = lib.dividir(a, b)
                print(f"División: {resultado}")
            guardar_resultado("dividir", f"{a}, {b}", resultado)
        
        elif opcion == "5":
            pais = input("Ingresá el código del país (ej: ARG, BRA, MEX): ").upper()
            gini = obtener_gini(pais)
            if gini is not None:
                gini_float = ctypes.c_float(gini)
                print(f"Gini original desde API: {gini_float.value}")
                nuevo_valor = lib.sumar_uno(gini_float)
                print(f"Gini + 1 con ASM: {nuevo_valor}")
            guardar_resultado(f"API + sumar_uno ({pais})", gini_float.value, nuevo_valor)


        elif opcion == "0":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intentá de nuevo.")

# Ejecutar el menú
menu()
