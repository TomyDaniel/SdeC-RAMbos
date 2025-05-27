# **Informe del Proyecto TP3: Modo Protegido**

**Grupo/Autor:** Rambos
**Materia:** Sistemas de Computación
**Alumnos:**
*   Viale, Sofia
*   Daniel, Tomas G

**Docentes:**
*   Solinas, Miguel A.
*   Jorge, Javier

---

# Desafio 1:

`checkinstall` es una herramienta de línea de comandos para sistemas Linux que **facilita la creación de paquetes binarios** (como `.deb` para Debian/Ubuntu, `.rpm` para Fedora/CentOS, o `.tgz` para Slackware) a partir de software compilado desde su código fuente.

## ¿Para qué sirve? El problema que resuelve:

Cuando compilas software desde el código fuente, el proceso típico es:
1.  `./configure` (o `cmake .` u otro)
2.  `make`
3.  `sudo make install`

El comando `sudo make install` copia los archivos compilados directamente en tu sistema (por ejemplo, en `/usr/local/bin`, `/usr/local/lib`, etc.). El problema con este método es:

1.  **Difícil desinstalación:** El gestor de paquetes de tu sistema (como `apt` o `yum`) no tiene ni idea de que este software ha sido instalado. Para desinstalarlo, tendrías que ir al directorio fuente y ejecutar `sudo make uninstall` (si el desarrollador lo incluyó y funciona bien), o borrar manualmente cada archivo, lo cual es propenso a errores y puede dejar archivos huérfanos.
2.  **Sin seguimiento:** No hay una forma fácil de saber qué archivos pertenecen a qué software instalado manualmente, ni de actualizarlo o gestionarlo como otros paquetes del sistema.
3.  **Posibles conflictos:** Puede sobrescribir archivos de otros paquetes sin que el sistema lo sepa, causando problemas.

## La solución que ofrece `checkinstall`:

`checkinstall` se ejecuta *en lugar de* `sudo make install` (o justo después de `make`, antes de instalar). Lo que hace es:

1.  **Observar el proceso de instalación:** Ejecuta el comando `make install` (o el que le indiques) en un entorno controlado y observa qué archivos se van a instalar y dónde.
2.  **Crear un paquete:** En lugar de instalar los archivos directamente, los empaqueta en un formato nativo de tu distribución (por ejemplo, un archivo `.deb` si estás en Debian/Ubuntu). Este paquete contiene los archivos compilados y la información sobre dónde deben ir.
3.  **Instalar el paquete (opcional):** Por defecto, después de crear el paquete, `checkinstall` también lo instala usando el gestor de paquetes de tu sistema (como `dpkg -i paquete.deb`).

## Beneficios de usar `checkinstall`:

*   **Desinstalación limpia:** Como el software se instala a través de un paquete, puedes desinstalarlo fácilmente usando tu gestor de paquetes (ej: `sudo apt remove nombre_del_paquete`).
*   **Integración con el sistema:** El software instalado aparece en la lista de paquetes de tu sistema, permitiendo una mejor gestión.
*   **Facilidad de uso:** Es mucho más sencillo que crear manualmente los archivos de especificación para `dpkg-buildpackage` o `rpmbuild` si solo quieres una forma rápida de empaquetar software para tu propio uso.
*   **Reinstalación / Actualización:** Si recompilas una nueva versión, puedes crear un nuevo paquete con `checkinstall` y tu gestor de paquetes manejará la actualización.

## ¿Cómo se usa (ejemplo básico en un sistema Debian/Ubuntu)?

```bash
# Descargar y descomprimir el código fuente
tar xvf software-1.0.tar.gz
cd software-1.0

# Configurar (ajustar prefijo si es necesario, ej: ./configure --prefix=/usr)
./configure

# Compilar
make

# En lugar de "sudo make install", usar checkinstall:
sudo checkinstall
# O, más explícitamente, decirle a checkinstall qué comando de instalación ejecutar:
# sudo checkinstall make install
```

# Desafío 2:

A continuación, se presentan las respuestas correspondientes a las preguntas del desafío.

## ¿Qué funciones tiene disponible un programa y un módulo?
### Programa (espacio de usuario)
Un programa en espacio de usuario tiene acceso a:

* Funciones proporcionadas por bibliotecas estándar (por ejemplo, ```libc``` en sistemas Unix).

* Servicios del sistema operativo mediante llamadas al sistema (como ```read()```, ```write()```, ```open()```, ```fork()```, entre otras).

* Interfaces de comunicación con el kernel a través de archivos en ```/proc``` y ```/sys```, y archivos de dispositivo en ```/dev```.

* Un programa no tiene acceso directo al hardware ni puede ejecutar instrucciones privilegiadas.

### Módulo (espacio del kernel)
Un módulo del kernel tiene acceso a:

* Funciones internas del kernel, como:

  * Gestión de memoria (```kmalloc()```, ```kfree()```)

   * Registro de dispositivos (```register_chrdev()```,``` register_netdev()```)

    * Manejo de interrupciones (```request_irq()```)

    * Funciones de sincronización (```spin_lock()```, ```mutex_lock()```)

* Acceso directo a hardware y estructuras internas del sistema operativo.

Un módulo puede influir directamente sobre el funcionamiento del sistema, por lo que debe ser desarrollado y probado con extremo cuidado.

## Espacio de usuario o espacio del kernel
### Espacio de usuario
* Es el entorno de ejecución de los programas y aplicaciones comunes.

* Posee acceso restringido al hardware y debe utilizar llamadas al sistema para interactuar con recursos protegidos.

* Cada proceso en espacio de usuario está aislado del resto, lo cual incrementa la seguridad y estabilidad del sistema.

### Espacio del kernel
* Es el entorno en el que se ejecutan el núcleo del sistema operativo y sus módulos cargados.

* Posee privilegios elevados, permitiendo acceso completo a la memoria, dispositivos y funciones internas del sistema.

* Todos los módulos comparten el mismo espacio de direcciones del kernel, lo que puede causar fallos críticos si no se manejan correctamente.

## Espacio de datos
El espacio de datos se refiere a la región de memoria utilizada por un programa o módulo para almacenar:

* Variables globales y estáticas.

* Datos inicializados y no inicializados (segmentos ```.data``` y ```.bss```, respectivamente).

### En espacio de usuario
* Cada proceso tiene su propio espacio de datos privado y protegido.

### En espacio del kernel
* Todos los módulos comparten el espacio de datos del kernel.

* Es necesario implementar mecanismos de sincronización adecuados para evitar condiciones de carrera o corrupción de datos.

## Drivers. Investigación sobre el contenido de ``` /dev```

### Drivers (controladores)
* Son componentes del kernel que permiten al sistema operativo interactuar con dispositivos de hardware (como discos, placas de red, teclados, etc.).

* Se implementan comúnmente como módulos del kernel.

* Traducen solicitudes de alto nivel (por ejemplo, una lectura de archivo) en instrucciones específicas para el hardware.

### Contenido de ```/dev```
El directorio ```/dev``` contiene archivos de dispositivo que representan interfaces hacia dispositivos de hardware o virtuales. Estos archivos permiten a los procesos de usuario acceder a dispositivos como si fueran archivos comunes.

### Tipos principales de dispositivos:
* Dispositivos de carácter: permiten operaciones de lectura/escritura secuencial, byte por byte (ej:``` /dev/tty```, ```/dev/random```).

* Dispositivos de bloque: permiten acceso a datos en bloques (ej: discos duros, como ```/dev/sda```).

* Dispositivos virtuales: no corresponden a hardware físico, pero son útiles para operaciones especiales (ej: ```/dev/null```, ```/dev/zero```, ```/dev/loop0```).

El acceso a estos dispositivos suele gestionarse mediante funciones estándar como ```open()```, ```read()```, ```write()``` y ```ioctl()```, que son redirigidas internamente por el kernel al driver correspondiente.


----------------------------------------


## 1)  ¿Qué diferencias se pueden observar entre los dos modinfo?

Al comparar la información obtenida mediante `modinfo` para mi módulo `mimodulo.ko` y el módulo del sistema `des_generic.ko.zst`, se observan varias diferencias significativas que reflejan su distinto origen y propósito. Mientras que `mimodulo.ko` se localiza en mi directorio de desarrollo (`/home/tomy/kenel-modules/part1/module/mimodulo.ko`) y posee metadatos como autor ("Catedra de SdeC") y descripción ("Primer modulo ejemplo") definidos por mí, `des_generic.ko.zst` reside en la ruta estándar del kernel (`/lib/modules/6.8.0-60-generic/kernel/crypto/des_generic.ko.zst`) con autoría ("Dag Arne Osvik <da@osvik.no>") y descripción ("DES & Triple DES EDE Cipher Algorithms") propias de su desarrollo oficial.

Una distinción clave es que `des_generic.ko.zst` muestra el atributo `intree: Y`, confirmando que es un módulo compilado como parte del árbol de fuentes del kernel, un atributo ausente en mi módulo externo. Además, `des_generic.ko.zst` presenta múltiples alias (como `crypto-des`, `des3_ede`), indica una dependencia del módulo `libdes`, y, crucialmente, contiene información detallada de firma digital (`sig_id`, `signer: Build time autogenerated kernel key`, `sig_key`, `sig_hashalgo`, `signature`). Estos campos de firma, ausentes en `mimodulo.ko` (que no está firmado), son característicos de los módulos distribuidos con el kernel para garantizar su integridad. Ambos módulos comparten una cadena `vermagic` idéntica (`6.8.0-60-generic SMP preempt mod_unload modversions`), lo cual es esencial y confirma su compatibilidad con el mismo kernel en ejecución. Mi módulo también muestra un `srcversion` (`C6390D617B2101FB1B600A9`), mientras que `des_generic.ko.zst` tiene su propio `srcversion` (`B56606AD918CF0074D320DB`), reflejando las fuentes específicas desde las que cada uno fue compilado.

## 2) ¿Qué drivers/módulos están cargados en sus propias PCs?
Cada integrante del grupo ejecutó lsmod para obtener la lista de módulos cargados en sus respectivos equipos. Luego, se generaron archivos lsmod_<nombre>.txt y se subieron al repositorio.

Tuvimos una sola computadora disponible con linux, por lo que usamos `lsmod` para encontrar todos los drivers y modulos de la PC que se uso. El mismo se encuentra en un archivo **.txt**

## 3) ¿Cuáles no están cargados pero están disponibles? ¿Qué pasa cuando el driver de un dispositivo no está disponible?
Se listaron los módulos disponibles pero no cargados mediante:

```
bash
find /lib/modules/$(uname -r) -name '*.ko*'
```

Un módulo puede estar disponible pero no cargado si el hardware asociado no está presente, o si no se ha detectado automáticamente. Cuando el controlador (driver) de un dispositivo no está disponible, el sistema:

- No lo puede inicializar.

- No crea la entrada correspondiente en /dev.

- Muestra el dispositivo como "desconocido" en herramientas como lspci o lsusb.

- El hardware queda inoperativo.


## 4) Ejecutar hwinfo en una PC real
Se ejecutó el siguiente comando en una máquina física:

```
bash
sudo hwinfo --short > hwinfo_<nombre>.txt
```
El reusltado de la ejecucion se encuentra subido en el  archivo `hwinfo.txt`

## 5) ¿Qué diferencia existe entre un módulo y un programa?

Los módulos del kernel y los programas de usuario son componentes de software fundamentalmente distintos dentro de un sistema operativo.

Un módulo del kernel se ejecuta en el espacio del kernel, lo que le otorga privilegios máximos y acceso directo a todo el hardware y la memoria del sistema. Su propósito principal es extender la funcionalidad del propio kernel, actuando comúnmente como drivers de dispositivos, sistemas de archivos o protocolos de red. Utilizan APIs internas del kernel y un error grave en un módulo puede provocar un fallo completo del sistema (Kernel Panic). Los módulos pueden ser cargados y descargados dinámicamente mientras el sistema está en funcionamiento.

Por el contrario, un programa de usuario se ejecuta en el espacio de usuario, un entorno aislado con privilegios restringidos. Los programas interactúan con el hardware de forma indirecta, solicitando servicios al kernel a través de llamadas al sistema y utilizando bibliotecas de usuario. Su propósito es realizar tareas específicas para el usuario, como un editor de texto o un navegador web. Un error en un programa de usuario generalmente solo afecta a ese programa, provocando su cierre, pero no desestabiliza el sistema operativo. Los programas se inician como procesos, realizan su función y luego terminan.
En esencia, los módulos son extensiones de bajo nivel y alta confianza del sistema operativo, mientras que los programas son aplicaciones de nivel superior que operan dentro de los límites seguros establecidos por el kernel.

## 6) ¿Cómo ver la lista de llamadas al sistema de un hello world?

Para observar las llamadas al sistema que un programa "Hello, world!" en C realiza, se utiliza la utilidad `strace`. Después de compilar un archivo `hello.c` simple que imprime "Hello, world!\n" usando `printf`, se ejecuta con `strace ./hello`. La salida resultante (mostrada parcialmente a continuación) revela la interacción detallada entre el programa y el kernel:

```
execve("./hello", ["./hello"], 0x7ffe10cde810 /* 46 vars */) = 0
brk(NULL) = 0x5ba607ae6000
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7d7fbb18a000
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=80851, ...}) = 0
mmap(NULL, 80851, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7d7fbb176000
close(3) = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\220\243\2\0\0\0\0\0"..., 832) = 832
mmap(NULL, 2170256, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7d7fbae00000
mmap(0x7d7fbae28000, 1605632, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x28000) = 0x7d7fbae28000
mmap(0x7d7fbafb0000, 323584, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1b0000) = 0x7d7fbafff000
mmap(0x7d7fbafff000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1fe000) = 0x7d7fbafff000
mmap(0x7d7fbb005000, 52624, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7d7fbb005000
close(3) = 0
arch_prctl(ARCH_SET_FS, 0x7d7fbb173740) = 0
mprotect(0x7d7fbafff000, 16384, PROT_READ) = 0
write(1, "Hello, world!\n", 14) = 14
exit_group(0) = ?
```

Análisis de las llamadas al sistema clave observadas:

1.  **`execve("./hello", ...)`**: Esta es la primera llamada, donde el kernel carga y comienza la ejecución del programa `hello`.
2.  **`brk(NULL)` y `brk(0x5ba607b07000)`**: Estas llamadas gestionan el *break* de datos del programa, que es el final del segmento de datos. Se utilizan para la asignación de memoria del heap.
3.  **`mmap(...)`**: Se realizan múltiples llamadas `mmap`. Estas se utilizan para varias tareas de mapeo de memoria, incluyendo la asignación de memoria anónima, y fundamentalmente para mapear las bibliotecas compartidas necesarias (como `libc.so.6`) en el espacio de direcciones del proceso.
4.  **`openat(...)`, `fstat(...)`, `read(...)`, `close(...)`**: Estas llamadas están involucradas en la localización, apertura, lectura y cierre de archivos. En este contexto, son cruciales para que el enlazador dinámico encuentre y cargue la biblioteca estándar de C (`libc.so.6`), que contiene la función `printf`.
5.  **`arch_prctl(ARCH_SET_FS, ...)`**: Establece la base del segmento FS, a menudo utilizado para el almacenamiento local de hilos (Thread-Local Storage).
6.  **`mprotect(...)`**: Cambia los permisos de protección de regiones de memoria. Por ejemplo, después de cargar el código de una biblioteca, sus segmentos de datos pueden necesitar permisos de escritura, mientras que los segmentos de código se marcan como solo lectura y ejecutables.
7.  **`write(1, "Hello, world!\n", 14)`**: Esta es la llamada al sistema fundamental que realiza la E/S. El primer argumento `1` es el descriptor de archivo para la salida estándar (stdout), `"Hello, world!\n"` es el buffer a escribir, y `14` es el número de bytes. Esta es la acción que efectivamente muestra el mensaje en la terminal.
8.  **`exit_group(0)`**: Esta llamada termina todos los hilos del proceso y el proceso mismo, devolviendo un código de estado `0` (que indica éxito) al sistema operativo.

Por lo tanto, `strace` nos permite visualizar cómo un programa simple como "Hello, world!" interactúa con el kernel para realizar tareas como la gestión de memoria, la carga de bibliotecas y la E/S a la terminal, todo a través de llamadas al sistema.
