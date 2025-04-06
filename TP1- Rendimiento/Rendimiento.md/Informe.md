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