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