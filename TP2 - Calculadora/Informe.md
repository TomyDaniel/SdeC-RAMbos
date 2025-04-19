# Informe del Proyecto TP2: Calculadora GINI (ASM/C/Python con Puente 64/32 bits)

**Grupo/Autor:** *RAMbos*  
**Materia:** Sistemas de Computación  
**Alumnos:**
- Viale, Sofia
- Daniel, Tomas G  

**Docentes:**
- Solinas, Miguel A.
- Jorge, Javier

## 1. Introducción

Este documento describe el desarrollo y la implementación del Trabajo Práctico N° 2 (TP2). El proyecto consiste en una aplicación que integra lenguajes de programación de diferentes niveles (Ensamblador x86, C y Python) para realizar cálculos numéricos. Específicamente, se enfoca en la implementación de operaciones aritméticas básicas y un procesamiento particular del índice GINI de desigualdad económica, obtenido desde una API web externa.

El objetivo principal es demostrar la interoperabilidad entre estos lenguajes: Ensamblador (NASM, 32 bits) para cálculos de bajo nivel optimizados o específicos (incluyendo punto flotante), C como capa de enlace (wrapper) para compilar una biblioteca compartida (`.so`), y Python como lenguaje de alto nivel para la interfaz de usuario, la lógica de aplicación y la interacción con servicios web.

Una característica técnica clave de esta implementación es el uso de la biblioteca `msl-loadlib` para establecer un puente entre un cliente Python ejecutándose en un entorno de 64 bits y la biblioteca compartida C/Ensamblador compilada para 32 bits, superando las limitaciones de carga directa entre arquitecturas diferentes mediante un mecanismo cliente-servidor inter-proceso.

## 2. Objetivos del Proyecto

Los objetivos específicos alcanzados en este proyecto son:

*   Implementar funciones aritméticas básicas (suma, promedio, multiplicación, división) en Ensamblador x86 (NASM, 32 bits), utilizando la Unidad de Punto Flotante (FPU).
*   Implementar una función específica en Ensamblador (`procesar_gini_asm`) para procesar un valor GINI (convertir de `float` a `int` y sumar 1).
*   Asegurar que las rutinas Ensamblador cumplan con la convención de llamada estándar de C (`cdecl`) para 32 bits (argumentos por pila, resultado float en `st(0)` o int en `EAX`).
*   Crear una capa de enlace (wrapper) en C (`libgini_wrapper.c`) para exponer las funciones de Ensamblador de forma organizada y compilarlas en una biblioteca compartida (`libgini.so`).
*   Desarrollar un cliente en Python (`gini_cliente.py`) con una interfaz de menú de consola para interactuar con el usuario.
*   Integrar una llamada a una API web externa (Banco Mundial) desde Python (`API.py`) para obtener datos reales del índice GINI.
*   Implementar un mecanismo para superar la incompatibilidad de arquitecturas entre Python (64 bits) y la biblioteca C/ASM (32 bits) utilizando `msl-loadlib` (cliente 64 bits, servidor 32 bits).
*   Gestionar el proceso completo de compilación y enlace del código C y Ensamblador mediante un `Makefile` robusto.
*   Configurar el proyecto para facilitar la depuración del código C y Ensamblador (especialmente la interacción C-ASM) usando GDB.
*   Registrar las operaciones realizadas por el usuario y sus resultados en un archivo de texto (`resultados_gini.txt`).

## 3. Tecnologías Utilizadas

*   **Lenguajes**:
    *   Ensamblador (`NASM syntax`, x86 32-bit, FPU)
    *   C (`GCC`)
    *   Python 3
*   **Herramientas de Compilación y Depuración**:
    *   `make` (para automatización de build)
    *   `gcc` (compilador C, con flags `-m32` y `-fPIC`)
    *   `nasm` (ensamblador, con flag `-f elf32`)
    *   `gdb` (depurador)
*   **Bibliotecas Python**:
    *   `msl-loadlib` (para puente 64/32 bits cliente-servidor)
    *   `ctypes` (utilizado internamente por el servidor 32 bits para cargar `libgini.so`)
    *   `requests` (para realizar consultas a la API web)
    *   `datetime` (para registrar timestamps)
*   **API Externa**: API REST del Banco Mundial (para datos del índice GINI).
*   **Sistema Operativo**: Linux (ej. Ubuntu 22.04 64 bits) con soporte `multilib` instalado (requerido para compilar y ejecutar código de 32 bits, incluyendo el intérprete Python 32 bits para `msl-loadlib`).

## 4. Arquitectura y Estructura del Proyecto

El proyecto se organiza en la siguiente estructura de directorios y componentes principales:

```text
TP2 (Raíz)/
  |-- Informe.md           # (Este informe)
  |-- Makefile             # Script para compilación, ejecución y gestión
  |-- README.md            # Documentación general y resumen
  |-- generate_sumary.py   # Script auxiliar Python para generar resúmenes
  |-- resultados_gini.txt  # Archivo de log con los resultados de las operaciones
  |-- test_procesador_debug # Ejecutable C 32 bits para depuración (generado por make)
  |-- obj/                   # Directorio para archivos objeto (generado por make)
  |-- libgini.so           # Biblioteca compartida 32 bits (generada por make)
.venv/                    # Directorio del entorno virtual de Python (opcional pero recomendado)
  |-- ...                  # Contenido del venv
C/                        # Código fuente en C
  |-- libgini_wrapper.c    # Wrapper C para las funciones ASM
  |-- test_procesador.c    # Programa C para probar directamente `procesar_gini_asm`
Test Memory/              # Directorio con pruebas iniciales/aisladas (posiblemente obsoletas)
  |-- test.c               # Código C de prueba (parece probar sumar_uno, posiblemente versión inicial)
Ensamblador/              # Código fuente en Ensamblador (NASM 32 bits)
  |-- dividir.asm          # Implementación de división de punto flotante (FPU)
  |-- multiplicar.asm      # Implementación de multiplicación de punto flotante (FPU)
  |-- procesar_gini.asm    # Implementación del procesamiento GINI (float -> int + 1)
  |-- promedio.asm         # Implementación de promedio de punto flotante (FPU)
  |-- sumar_uno.asm        # Implementación de suma de 1.0 a un float (FPU)
Python/                   # Código fuente en Python
  |-- API.py               # Módulo para obtener datos GINI de la API del Banco Mundial
  |-- gini_cliente.py      # Cliente Python 64 bits (Interfaz de usuario, usa msl-loadlib)
  |-- gini_server.py       # Servidor Python 32 bits (Carga libgini.so con ctypes, usa msl-loadlib)
```

## 5. Descripción Detallada de Componentes

*   **Ensamblador (`Ensamblador/`)**:
    *   Contiene el núcleo lógico de bajo nivel implementado en NASM para x86 32 bits.
    *   **`sumar_uno`**: Recibe un `float`, le suma `1.0` usando `fld1` y `faddp`. Devuelve `float` en `st(0)`.
    *   **`promedio`**: Recibe dos `float`, los suma (`faddp`), divide por `2.0` (`fdivp`). Devuelve `float` en `st(0)`.
    *   **`multiplicar`**: Recibe dos `float`, los multiplica (`fmulp`). Devuelve `float` en `st(0)`.
    *   **`dividir`**: Recibe dos `float`, los divide (`fdivp`). Devuelve `float` en `st(0)`.
    *   **`procesar_gini_asm`**: Recibe un `float`, lo convierte a entero truncado (`fistp dword [esp]`), mueve el entero de la pila a `EAX` (`pop eax`), le suma 1 (`add eax, 1`). Devuelve `int` en `EAX`.
    *   Todas las funciones siguen el prólogo (`push ebp; mov ebp, esp`) y epílogo (`mov esp, ebp; pop ebp; ret` o similar) estándar para la gestión del stack frame bajo la convención `cdecl`.

*   **C (`C/`)**:
    *   `libgini_wrapper.c`: Actúa como capa de enlace. Declara las funciones ASM como `extern` con sus prototipos correctos (ej. `extern float promedio(float a, float b);`, `extern int procesar_gini_asm(float g);`). Define la función `procesar_gini_final(float valor_gini)` que simplemente llama a `procesar_gini_asm` y retorna su valor entero. Las demás funciones ASM son accesibles directamente por su nombre desde la biblioteca compartida.
    *   `test_procesador.c`: Programa C simple y autocontenido para probar específicamente la función `procesar_gini_asm`. Llama a la función ASM con un valor float de prueba, imprime el resultado entero. Esencial para la depuración aislada de la lógica C-ASM con GDB.

*   **Python (`Python/`)**:
    *   `API.py`: Define la función `obtener_gini(pais)` que usa `requests` para consultar la API del Banco Mundial (`SP.POP.TOTL` -> `SI.POV.GINI`). Maneja la respuesta JSON, busca el último valor GINI no nulo y lo retorna como `float`. Incluye manejo básico de errores de conexión/datos.
    *   `gini_server.py`: Implementa un servidor 32 bits (`GiniServer32`) usando `msl.loadlib.Server32`. Este script *debe* ser ejecutado por un intérprete Python de 32 bits. Carga la biblioteca `./libgini.so` (32 bits) usando `ctypes.CDLL`. Define explícitamente los tipos de argumentos (`argtypes`) y el tipo de retorno (`restype`) para cada función C/ASM expuesta (ej. `self.lib.promedio.argtypes = [c_float, c_float]`, `self.lib.promedio.restype = c_float`, `self.lib.procesar_gini_final.argtypes = [c_float]`, `self.lib.procesar_gini_final.restype = c_int`). Expone estas funciones para llamadas remotas desde el cliente.
    *   `gini_cliente.py`: Implementa el cliente 64 bits (`GiniClient64`) usando `msl.loadlib.Client64`. Este script se ejecuta con el intérprete Python estándar (64 bits). Se conecta al `GiniServer32` (iniciándolo automáticamente si es necesario). Proporciona el menú interactivo al usuario. Recoge entradas, llama a los métodos del cliente (ej. `client.promedio(a, b)`), que a su vez usan `self.request32(...)` para enviar la solicitud al servidor 32 bits. Muestra los resultados recibidos del servidor. Llama a `API.py` para obtener el GINI. Llama a `guardar_resultado` para registrar la operación en `resultados_gini.txt`.

*   **Build System (`Makefile`)**: Automatiza la compilación, enlace, ejecución y limpieza.
    *   Define variables para compiladores (`CC=gcc`, `NASM=nasm`), flags (`CFLAGS = -m32 -g3 -fPIC`, `NASMFLAGS = -f elf32 -g -F dwarf`, `LDFLAGS = -shared`, `LDFLAGS_EXEC = -m32 -g3`), directorios y nombres de archivos.
    *   **Targets Principales:**
        *   `all` (default): Construye `libgini.so` y `test_procesador_debug`.
        *   `$(TARGET_LIB)` (`libgini.so`): Ensambla los `.asm` a `.o` (en `obj/`), compila `libgini_wrapper.c` a `.o` (en `obj/`), y los enlaza en una biblioteca compartida 32 bits.
        *   `$(TARGET_TEST_DEBUG)` (`test_procesador_debug`): Compila `test_procesador.c` y lo enlaza con `procesar_gini.o` para crear un ejecutable de depuración 32 bits.
    *   **Targets Auxiliares:**
        *   `run`: Ejecuta el cliente Python 64 bits (`python3 Python/gini_cliente.py`).
        *   `clean`: Elimina `obj/`, `libgini.so`, `test_procesador_debug` y otros archivos temporales.
        *   `gdb`: Inicia GDB con el ejecutable de prueba `test_procesador_debug`.
        *   `debug`: Inicia GDB con el ejecutable de prueba y establece breakpoints útiles automáticamente antes de ejecutar.

*   **Logging (`resultados_gini.txt`)**: Archivo de texto donde el `gini_cliente.py` guarda un registro de cada operación realizada, incluyendo timestamp, tipo de operación, valores de entrada y resultado obtenido.

## 6. Flujo de Ejecución Principal (Cliente-Servidor con `msl-loadlib`)

1.  **Compilación:** El desarrollador ejecuta `make` (o `make all`) en la terminal. El `Makefile` compila los fuentes ASM y C, generando la biblioteca `libgini.so` (32 bits) y el ejecutable `test_procesador_debug` (32 bits).
2.  **Ejecución:** El usuario ejecuta `make run` o directamente `python3 Python/gini_cliente.py`.
3.  **Inicio Cliente-Servidor:**
    *   El `GiniClient64` (64 bits) se inicializa.
    *   Usando `msl-loadlib`, intenta conectarse al `GiniServer32`. Si no está corriendo, `msl-loadlib` busca un intérprete Python de 32 bits (`python3.x-32` o `python3:i386`) y lo utiliza para ejecutar el script `Python/gini_server.py` en un proceso separado.
    *   El `GiniServer32` (32 bits) se inicia en su propio proceso, carga la biblioteca `libgini.so` (32 bits) usando `ctypes`, y configura los `argtypes`/`restype` de las funciones C/ASM. Queda a la espera de peticiones.
4.  **Interacción del Usuario:** El `GiniClient64` muestra el menú interactivo.
5.  **Llamada a Función Remota (Ejemplo: Promedio):**
    *   El usuario selecciona "Promedio" e ingresa dos números.
    *   El `GiniClient64` llama a su método `client.promedio(num1, num2)`.
    *   Este método internamente llama a `self.request32('promedio', num1, num2)`.
    *   `msl-loadlib` serializa los argumentos y envía la petición al proceso `GiniServer32` a través de comunicación inter-proceso (IPC).
    *   El `GiniServer32` recibe la petición, deserializa los argumentos y llama al método `promedio` del servidor.
    *   El método `promedio` del servidor llama a la función C/ASM cargada: `self.lib.promedio(num1, num2)`. `ctypes` gestiona la llamada a la función nativa de 32 bits.
    *   La rutina `promedio.asm` se ejecuta utilizando la FPU.
    *   El resultado (`float`) retorna a través de `ctypes` al `GiniServer32`.
    *   El `GiniServer32` serializa el resultado y lo envía de vuelta al `GiniClient64` mediante IPC.
    *   `msl-loadlib` en el cliente recibe la respuesta y la deserializa.
    *   El `GiniClient64` recibe el resultado final y lo muestra al usuario.
6.  **Operación GINI:** Si se elige la opción 5, el cliente primero llama a `obtener_gini` de `API.py` (ejecutándose en el proceso 64 bits) para obtener el valor. Luego, llama a `client.procesar_gini_final(valor_gini)`, que sigue el mismo flujo cliente-servidor descrito antes para invocar `procesar_gini_asm` en el entorno 32 bits.
7.  **Registro:** Para cada operación, el `GiniClient64` llama a `guardar_resultado` para añadir una entrada al archivo `resultados_gini.txt`.
8.  **Finalización:** Cuando el usuario sale del cliente, `msl-loadlib` gestiona el cierre de la conexión IPC y la finalización del proceso `GiniServer32`.

## 7. Compilación, Pruebas y Depuración

*   **Compilación**: `make` o `make all` construye los artefactos necesarios (`libgini.so`, `test_procesador_debug`).
*   **Ejecución Principal**: `make run` inicia el cliente Python (`gini_cliente.py`).
*   **Limpieza**: `make clean` elimina los archivos generados (`obj/`, `libgini.so`, `test_procesador_debug`).
*   **Prueba Unitaria (C-ASM)**: Se puede ejecutar `./test_procesador_debug` directamente (después de `make`) para verificar la función `procesar_gini_asm` de forma aislada.
*   **Depuración (C-ASM con GDB)**:
    *   `make gdb`: Abre GDB cargando `test_procesador_debug`. El desarrollador puede establecer breakpoints manualmente (ej., `b main`, `b procesar_gini_asm`, `r` para ejecutar). Permite inspeccionar registros (incluyendo FPU), memoria y el flujo entre C y ASM.
    *   `make debug`: Similar a `gdb`, pero utiliza un script GDB (`-x .gdbinit` implícito o comandos directos) para establecer breakpoints automáticamente en `main` (en C), antes y después de la llamada a ASM en `test_procesador.c`, y al inicio de la función ASM (`procesar_gini_asm`). Luego inicia la ejecución (`run`) dentro de GDB, facilitando el análisis paso a paso.
*   **Prueba Integrada (Python-C-ASM)**: Ejecutar `make run` y utilizar las diferentes opciones del menú prueba la integración completa a través del puente `msl-loadlib`. Los resultados se verifican en la consola y en `resultados_gini.txt`.

## 8. Resultados

La ejecución del sistema (`make run`) presenta correctamente el menú interactivo. Todas las operaciones matemáticas (suma, promedio, multiplicación, división) funcionan como se espera, delegando el cálculo a las rutinas FPU en ensamblador a través del puente C y `msl-loadlib`. La obtención del índice GINI desde la API del Banco Mundial y su posterior procesamiento mediante la función `procesar_gini_asm` también se realizan con éxito.

Cada operación ejecutada queda registrada en el archivo `resultados_gini.txt`, por ejemplo:

```
2025-04-15 10:30:01 - Operación: Promedio, Entrada: (10.5, 20.5), Resultado: 15.5
2025-04-15 10:30:15 - Operación: GINI (Argentina), Entrada GINI: 42.3, Resultado Procesado: 43
2025-04-15 10:30:30 - Operación: Dividir, Entrada: (100.0, 0.0), Error: División por cero no permitida.
...
```


## 9. Conclusión

El proyecto TP2 ha sido completado satisfactoriamente, demostrando la viabilidad y los mecanismos necesarios para integrar código Ensamblador x86 de 32 bits (con uso de FPU) con una aplicación Python moderna de 64 bits. La implementación de funciones de cálculo en bajo nivel, la creación de un wrapper en C y su compilación como biblioteca compartida, y la interacción desde Python se lograron según los objetivos.

La introducción de `msl-loadlib` fue crucial para superar la barrera de arquitecturas, proporcionando una solución elegante y funcional basada en un modelo cliente-servidor inter-proceso. El uso de un `Makefile` robusteció el proceso de desarrollo, compilación y depuración, mientras que la inclusión de pruebas unitarias en C y la facilidad para usar GDB permitieron verificar y refinar la lógica de bajo nivel. El registro de operaciones añade una capa de trazabilidad útil.

Este proyecto refuerza la comprensión de las convenciones de llamada, la gestión de tipos de datos entre lenguajes (especialmente `float` vs `int`), el uso de la FPU, y las técnicas para la interoperabilidad entre diferentes niveles de abstracción y arquitecturas en el desarrollo de software.
