# Universidad Nacional de Córdoba


## Trabajo Práctico N°1 SdeC


### Alumnos:
- **Daniel, Tomas G.**
- **Viale, Sofía**


### Docentes:
- **Jorge, Javier**
- **Solinas, Miguel**


---


## Introducción


En el siguiente trabajo, tenemos como objetivos:
- Evaluar el rendimiento de diferentes computadoras.
- Aplicar conocimientos sobre benchmark y performance de los procesadores de computadoras.
- Entender la utilidad de los tests de rendimiento y en qué situaciones elegir un componente sobre otro según el uso específico.


Como parte del trabajo, analizamos el rendimiento de tres procesadores distintos (**Intel Core i5-13600K, AMD Ryzen 9 5900X 12-Core y AMD Ryzen 9 7950X 16-Core**) en tareas de compilación del kernel de Linux. Para esto, se utilizó información de la página [OpenBenchmarking](https://openbenchmarking.org/test/pts/build-linux-kernel-1.15.0).


Otro experimento de rendimiento consistió en el uso de una **ESP32** a la que se le varió la frecuencia de operación para medir tiempos de procesamiento. Para esto, se utilizó la página [Wokwi](https://wokwi.com/projects/new/esp32), ya que no contamos con una ESP32 física. Se documentaron imágenes de los resultados obtenidos para su posterior análisis. Se realizo la experiencia con un modulo de **ESP32** con la cual se llegaron a los resultados mostrados posteriormente.


---


## Desarrollo


### Benchmarks


#### Distintos tipos de Benchmarks


Existen diversos tipos de benchmarks que se clasifican según el componente evaluado. A continuación, se describen los principales tipos:


#### **Benchmarks sintéticos**
Son pruebas controladas con código optimizado para una plataforma y arquitectura específica. Permiten realizar comparaciones directas ya que los test son consistentes en cada ejecución.


#### **Benchmarks reales**
Evalúan el rendimiento en condiciones de uso cotidiano, sin seguir patrones predefinidos. Son útiles para estimar la experiencia del usuario en tareas diarias.


Algunos ejemplos de benchmarks según el componente analizado:


- **Benchmark de CPU**: Evalúan la velocidad de cálculo y la eficiencia de ejecución en tareas simultáneas.
 - *Ejemplos de software*: Cinebench, Geekbench, PassMark.


- **Benchmark de GPU**: Analizan el rendimiento gráfico y el cálculo paralelo.
 - *Ejemplos de software*: 3DMark, FurMark, GeekBench 5.


- **Benchmark de Memoria RAM**: Miden velocidad de acceso, tasa de transferencia y latencia.
 - *Ejemplos de software*: MemTest 64, VMap.


- **Benchmark de almacenamiento**: Analizan el rendimiento de unidades SSD, HDD y NVMe.
 - *Ejemplos de software*: EaseUS Partition Master, CrystalDiskMark, ATTO Disk Benchmark.


- **Benchmark de red**: Evalúan el ancho de banda, latencia y estabilidad de conexión.
 - *Ejemplos de software*: Speedtest, iPerf, NetBench, Fast.


---


## Benchmark: Compilación del Kernel de Linux


Se compararon tres procesadores analizando el tiempo de compilación del kernel de Linux.


### **Ryzen 9 7950X**
- **Núcleos / Hilos**: 16 / 32
- **Precio**: ~ US$ 470
- **Tiempo de compilación**: 53s ± 3s
- **Rendimiento**: `Rend = 1/53 = 0.018`
- **Rendimiento por precio**: `RendPrec = Rend / Precio = 38.3 × 10⁻⁶`
- **TDP**: 170W
- **Rendimiento por watt**: `RendWatt = Rend / TDP = 105.88 × 10⁻⁶`


### **Ryzen 9 5900X**
- **Núcleos / Hilos**: 12 / 24
- **Precio**: ~ US$ 289.99
- **Tiempo de compilación**: 97s ± 7s
- **Rendimiento**: `Rend = 1/97 = 0.010`
- **Rendimiento por precio**: `RendPrec = Rend / Precio = 34.48 × 10⁻⁶`
- **TDP**: 105W
- **Rendimiento por watt**: `RendWatt = Rend / TDP = 95.23 × 10⁻⁶`


### **Intel i5-13600K**
- **Núcleos / Hilos**: 14 / 20
- **Precio**: ~ US$ 394.95
- **Tiempo de compilación**: 83s ± 3s
- **Rendimiento**: `Rend = 1/83 = 0.012`
- **Rendimiento por precio**: `RendPrec = Rend / Precio = 30.5 × 10⁻⁶`
- **TDP**: 125W
- **Rendimiento por watt**: `RendWatt = Rend / TDP = 2.4 × 10⁻⁶`


#### **Comparativa de rendimiento**


Si tomamos como referencia al **Ryzen 9 7950X**, calculamos la aceleración relativa:


- **Frente al Ryzen 9 5900X**: `97 / 53 = 1.83x`
- **Frente al i5 13600K**: `83 / 53 = 1.566x`


El **Ryzen 9 7950X** demuestra ser superior en términos de tiempo de compilación y eficiencia energética, aunque no es el más rentable en relación costo/rendimiento.


---

## Profiling


El objetivo de este estudio es analizar el rendimiento del código mediante herramientas de **profiling**. Para ello, utilizamos `gprof` para medir el tiempo de ejecución de las funciones en dos versiones de código escritas en **C**: `test_gprof.c` y `test_gprof_new.c`.


### Metodología


Para obtener los perfiles de ejecución seguimos estos pasos:


1. **Compilación del código con soporte para profiling:**


```
gcc -pg test_gprof.c -o test_gprof
gcc -pg test_gprof_new.c -o test_gprof_new
```


2. **Ejecución de los programas para generar los archivos de profiling:**


```
./test_gprof
./test_gprof_new
```


3. **Análisis del rendimiento con ``:**


```
gprof test_gprof gmon.out > profile_test_gprof.txt
gprof test_gprof_new gmon.out > profile_test_gprof_new.txt
```


### Analisis del codigo:


#### 🔹 Código `test_gprof.c`


Este código contiene varias funciones con bucles grandes, diseñados para consumir tiempo de CPU. Se destacan:


- `func1()`, con un bucle de `0xffffffff` iteraciones.
- `func2()`, con un bucle de `0xafffffff` iteraciones.
- `main()`, que también contiene un bucle antes de llamar a estas funciones.


**Resultados esperados en el profiling:** La mayor parte del tiempo de ejecución será consumido por `func1()` y `func2()` debido a la cantidad de iteraciones en sus bucles.


#### 🔹 Código `test_gprof_new.c`


Este archivo solo define `new_func1()`, que tiene:


- Un `printf()` para indicar su ejecución.
- Un bucle de `0xfffff66` iteraciones (menor que `func1()` en `test_gprof.c`).


**Resultados esperados en el profiling:** `new_func1()` tendrá un menor impacto en el tiempo total de ejecución debido a su menor cantidad de iteraciones.


### Resultados del profiling:


Se puede notar que `test_gprof_new.c` tiene un menor tiempo de ejecución en comparación con `test_gprof.c`, lo que era esperado debido a la menor cantidad de iteraciones en el bucle de `new_func1()`. La optimización de bucles es clave para mejorar el rendimiento.
Las experiencias se adjuntan en [profiling.md](profiling.md)




### Conclusion Profiling:


El uso de `gprof` nos permitió identificar qué funciones consumen más tiempo de ejecución. Se observó que reducir el número de iteraciones en los bucles disminuye significativamente el tiempo total del programa. Esta información es útil para optimizar el rendimiento de aplicaciones críticas en tiempo de ejecución.


En particular, `func1()` en `test_gprof.c` fue la función con mayor tiempo de procesamiento debido a su gran cantidad de iteraciones, mientras que `new_func1()` en `test_gprof_new.c` mostró una mejora significativa al reducir las iteraciones.


Este análisis demuestra la importancia de perfilar y optimizar el código para mejorar la eficiencia de ejecución.


---


## Medición de performance ESP32


Se analizó cómo varía el tiempo de ejecución al modificar la frecuencia del procesador en una **ESP32** simulada en [Wokwi](https://wokwi.com/).


### **Configuración**
Se ejecutó un código en Arduino para medir el tiempo de una función de suma de enteros a distintas frecuencias:
- **80 MHz**
- **160 MHz**
- **240 MHz**


El objetivo fue observar si el aumento de la frecuencia de la CPU produce una reducción proporcional en el tiempo de ejecución.


Los resultados obtenidos se muestran en la siguiente imagen:


![alt text](image.png)


Ademas de utilizar el simulador, pudimos tener acceso a una ESP32 fisica. Se testeo con el mismo codigo utilizado en el simulador y se noto una gran diferencia con respecto a los tiempos obtenidos entre uno y otro, siendo la placa mucho mas veloz que el simulador 

![alt text](image-1.png)

![alt text](image-2.png)


---


## Conclusión


- Al **aumentar la frecuencia** del microcontrolador, se observa una mejora en el rendimiento.
- Al **triplicar la frecuencia** (de 80 MHz a 240 MHz), los tiempos de ejecución se reducen en un factor cercano a **tres**.
- Las **operaciones en punto flotante** presentan tiempos de ejecución más altos que los enteros, debido a su mayor complejidad computacional.


Este trabajo permitió comprender mejor cómo varía el rendimiento en función de distintos factores en procesadores de computadora y microcontroladores.