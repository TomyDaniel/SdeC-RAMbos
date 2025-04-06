# Trabajo Práctico #2 – Calculadora de Índice GINI (ASM, C y Python)

**Grupo:** Viale, Sofia - Daniel, Tomas Gaston  
**Materia:** Sistemas de Computacion  
**Fecha:** Abril 2025  

---

##  1. Introducción

El presente trabajo práctico tiene como objetivo integrar conocimientos de bajo nivel (ensamblador NASM de 32 bits) con lenguajes de alto nivel (C y Python) para desarrollar una aplicación capaz de consultar datos reales desde una API REST y realizar cálculos sobre los mismos mediante rutinas en lenguaje ensamblador.

---

##  2. Objetivos

- Implementar rutinas matemáticas en lenguaje ensamblador.
- Integrar dichas rutinas desde un programa en C.
- Invocar la funcionalidad desde una interfaz Python.
- Utilizar una API REST para obtener valores del índice GINI en tiempo real.
- Cumplir con la convención de llamada `cdecl` pasando parámetros por stack y devolviendo resultados por el registro `EAX`.
- Mostrar con GDB el comportamiento del stack durante una llamada a función ASM.

---

##  3. Tecnologías utilizadas

- NASM 32 bits
- C (con `gcc` y compilación 32 bits)
- Python 3 (usando `ctypes` y `requests`)
- API REST del Banco Mundial
- GDB para debug y análisis de stack
- Sistema operativo: Ubuntu 22.04 (64 bits) con soporte multilib

---

##  4. Descripción del sistema implementado

El sistema está compuesto por tres capas:

###  a. Capa inferior: Ensamblador
Se implementaron las siguientes funciones matemáticas en NASM:
- `sumar_uno`: suma 1 al valor recibido.
- `multiplicar`: multiplica por 2.
- `dividir`: divide por 2.
- `promedio`: calcula el promedio entre dos valores.

Todas estas rutinas reciben parámetros por stack y devuelven resultados en EAX, respetando la convención `cdecl`.

###  b. Capa intermedia: C
El archivo `libgini_wrapper.c` contiene funciones que actúan como puente entre Python y ensamblador. Estas funciones llaman a las rutinas ASM y permiten compilar una biblioteca compartida (`libgini.so`).

###  c. Capa superior: Python
El programa `gini_cliente.py` presenta un menú interactivo y permite al usuario:
- Ingresar un valor manual o consultar el índice GINI desde una API REST (`API.py`).
- Seleccionar una operación matemática.
- Ver el resultado calculado por ASM, mostrado por pantalla.

---

##  5. Test unitario y uso de GDB

Se implementó un archivo `test/test_stack.c` independiente que permite:
- Llamar directamente a la función `sumar_uno` desde C.
- Visualizar el estado del stack antes, durante y después de la llamada.
- Usar GDB para observar el comportamiento real del stack y los registros.

**Compilación del test:**
```bash
nasm -f elf32 -o Ensamblador/sumar_uno.o Ensamblador/sumar_uno.asm
gcc -m32 -g -o test/test_stack test/test_stack.c Ensamblador/sumar_uno.o
```

**Uso con GDB:**
```bash
gdb test/test_stack
```

**Comandos útiles en GDB:**
```
break main
run
next
step
info registers
x/20x $esp
finish
```

---

##  6. Instrucciones de compilación y ejecución

### 1. Compilar funciones en ensamblador:
```bash
nasm -f elf32 -o Ensamblador/sumar_uno.o Ensamblador/sumar_uno.asm
...
```

### 2. Compilar biblioteca compartida:
```bash
gcc -m32 -fPIC -shared -o libgini.so C/libgini_wrapper.c Ensamblador/*.o
```

### 3. Ejecutar el programa en Python:
```bash
cd Python
python3 gini_cliente.py
```

---

##  7. Conclusión

El proyecto permitió reforzar los conceptos de interacción entre lenguajes de alto y bajo nivel, comprender en profundidad la convención `cdecl`, y aplicar técnicas de debugging con GDB. Además, se incorporó el uso de una API REST real, integrando conocimientos modernos de desarrollo web con programación de sistemas.


