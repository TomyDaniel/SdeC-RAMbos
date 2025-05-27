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

## 7) ¿Qué es un segmentation fault? ¿Cómo lo maneja el kernel y cómo lo hace un programa?

Un **segmentation fault** (falla de segmentación), a menudo abreviado como "segfault", es un tipo específico de error que ocurre cuando un programa intenta acceder a una ubicación de memoria a la que no tiene permiso para acceder, o intenta acceder a una ubicación de memoria de una manera que no está permitida (por ejemplo, escribir en una región de memoria de solo lectura). Es una forma de violación de acceso a la memoria de propósito general.

Las causas comunes de un segmentation fault incluyen:
*   Intentar desreferenciar un puntero `NULL`.
*   Intentar desreferenciar un puntero que ya ha sido liberado (`free`d) (puntero colgante o *dangling pointer*).
*   Intentar escribir más allá de los límites de un buffer asignado (desbordamiento de buffer o *buffer overflow*).
*   Intentar escribir en una sección de memoria de solo lectura (como el segmento de código).
*   Usar punteros no inicializados que apuntan a direcciones de memoria arbitrarias.

**¿Cómo lo maneja el kernel?**

Cuando ocurre un intento de acceso inválido a la memoria, la Unidad de Gestión de Memoria (MMU) del hardware detecta la violación y genera una excepción de hardware (una *page fault* o falta de página, que en este caso no se puede resolver). Esta excepción de hardware interrumpe la ejecución normal del programa y transfiere el control al kernel.

El kernel maneja esta excepción de la siguiente manera:
1.  **Notificación al Proceso:** El kernel determina que la falta de página se debe a un acceso ilegal y no a una página que simplemente necesita ser traída desde el disco (swapping).
2.  **Envío de una Señal:** El kernel envía una señal al proceso que causó la falla. La señal estándar para una falla de segmentación en sistemas POSIX (como Linux) es `SIGSEGV` (Señal 11).
3.  **Terminación del Proceso (por defecto):** Si el programa no tiene un manejador específico para la señal `SIGSEGV`, la acción por defecto del kernel para esta señal es terminar el proceso infractor. Esto es para proteger al resto del sistema de un programa que se está comportando mal y podría corromper datos o causar más inestabilidad.
4.  **Volcado de Núcleo (Core Dump) (opcional):** Si está configurado en el sistema (a través de `ulimit -c` o configuraciones del sistema), el kernel puede generar un archivo de "volcado de núcleo" o *core dump*. Este archivo es una instantánea del estado de la memoria del proceso en el momento de la falla. Los desarrolladores pueden usar herramientas de depuración (como GDB) con el ejecutable y el core dump para analizar la causa exacta del segmentation fault.

**¿Cómo lo maneja un programa?**

Un programa en espacio de usuario tiene opciones limitadas pero importantes sobre cómo "manejar" un `SIGSEGV` una vez que el kernel se lo envía:

1.  **Acción por Defecto (Terminación):** Como se mencionó, si el programa no hace nada especial, la acción por defecto es que el kernel termine el programa. Esto es lo que sucede la mayoría de las veces y es generalmente lo más seguro. El usuario típicamente verá un mensaje como "Segmentation fault (core dumped)" en la terminal.

2.  **Instalar un Manejador de Señales (Signal Handler):** Un programa puede registrar una función personalizada (un manejador de señales) para ser llamada cuando se recibe la señal `SIGSEGV`. Esto se hace usando la llamada al sistema `sigaction()` (o la más simple `signal()`, aunque `sigaction()` es preferida).
    *   **Limitaciones del Manejador:** Dentro de un manejador para `SIGSEGV`, las acciones que se pueden realizar de forma segura son muy limitadas. No se puede, por ejemplo, simplemente "corregir" el puntero y reintentar la operación que causó la falla, porque el estado del programa puede ser inconsistente.
    *   **Usos Comunes del Manejador:**
        *   **Limpieza controlada:** Intentar guardar cualquier trabajo crítico pendiente (si es posible y seguro), cerrar archivos, liberar algunos recursos antes de terminar. Esto debe hacerse con extremo cuidado, ya que la memoria del programa ya está en un estado corrupto.
        *   **Registro de información adicional (Logging):** Escribir información de diagnóstico más detallada en un archivo de log para ayudar a la depuración posterior.
        *   **Terminación controlada:** Después de realizar alguna limpieza mínima o logging, el manejador generalmente debe terminar el programa explícitamente (por ejemplo, llamando a `_exit()`) o reestablecer el manejador por defecto y volver a generar la señal para que el kernel termine el programa.
    *   **No se puede "ignorar" `SIGSEGV` de forma efectiva para continuar la ejecución normal:** Intentar simplemente retornar del manejador de `SIGSEGV` y continuar la ejecución del programa donde se quedó es generalmente una mala idea y a menudo resultará en otra falla de segmentación inmediatamente o en un comportamiento errático e impredecible, ya que la causa subyacente de la corrupción de memoria no se ha solucionado.

En resumen, el kernel detecta la violación de memoria a través del hardware, notifica al proceso mediante una señal (`SIGSEGV`), y por defecto termina el proceso. El programa puede optar por interceptar esta señal para realizar una limpieza limitada o registrar información antes de terminar, pero no puede "recuperarse" mágicamente de la condición de error subyacente que causó la falla de segmentación.

## 8) ¿Se animan a firmar un módulo del kernel? Documentación del proceso

Para asegurar que los módulos del kernel que desarrollamos puedan cargarse en un sistema con Secure Boot habilitado, procedimos a firmar nuestro módulo `mimodulo.ko`. A continuación, se detalla el proceso seguido.

###  Fase 1: Preparación y Generación de Claves

Como primera instancia, se verificó que Secure Boot estuviera activado en el sistema mediante el comando `mokutil --sb-state`.

![Estado de Secure Boot](img/SecureBoot.png)
*(Leyenda: La salida confirma que Secure Boot está habilitado.)*

Luego, se creó un directorio dedicado para almacenar las claves criptográficas que se generarían y, posteriormente, el módulo a firmar (aunque el módulo se firma en su ubicación original de compilación).
```bash
mkdir ~/module_signing_keys
cd ~/module_signing_keys
```

 A continuación, se generó un par de claves RSA de 4096 bits (una clave privada y un certificado X.509 público en formato DER) utilizando openssl. La clave privada se guardó como `signing_key.priv` y el certificado público como `signing_key.der`. El certificado se configuró con un Common Name (CN) "Mi Modulo Kernel Key" y una validez extensa.

 ``` 
 openssl req -new -x509 -newkey rsa:4096 -keyout signing_key.priv -outform DER -out signing_key.der -nodes -days 36500 -subj "/CN=Mi Modulo Kernel Key/"
 ```

 ![alt text](img/GeneracionClave.png)

### Fase 2: Registro de la Clave Pública (Enroll MOK)

Con la clave pública (`signing_key.der`) generada, el siguiente paso fue importarla al sistema para que UEFI/Shim la reconozca. Esto se hizo con el comando sudo `mokutil --import`

```
sudo mokutil --import ~/module_signing_keys/signing_key.der
```

Tras establecer la contraseña, se reinició el sistema con `sudo reboot`. Durante el proceso de arranque, antes de cargar el sistema operativo, apareció la interfaz del MOKManager (pantalla azul).
Se procedió de la siguiente manera en el MOKManager:

-    Se presionó una tecla para interactuar con la utilidad.

-   Se seleccionó la opción "**Enroll MOK**".

-   Se eligió "**Continue**" para ver las claves pendientes.

-   Se seleccionó la clave correspondiente a "Mi Modulo Kernel Key".

-   Se confirmó la inscripción seleccionando "**Yes**".

-   Se ingresó la contraseña establecida previamente con mokutil.

-   Finalmente, se seleccionó "**Reboot**" para reiniciar el sistema.

Una vez que el sistema arrancó completamente, se verificó que la clave se había inscrito correctamente en la base de datos de MOKs mediante el comando `mokutil --list-enrolled`.

```
tomy@tomy:~$ mokutil --list-enrolled
[key 1]
SHA1 Fingerprint: 76:a0:92:06:58:00:bf:37:69:01:c3:72:cd:55:a9:0e:1f:de:d2:e0
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            b9:41:24:a0:18:2c:92:67
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=GB, ST=Isle of Man, L=Douglas, O=Canonical Ltd., CN=Canonical Ltd. Master Certificate Authority
        Validity
            Not Before: Apr 12 11:12:51 2012 GMT
            Not After : Apr 11 11:12:51 2042 GMT
        Subject: C=GB, ST=Isle of Man, L=Douglas, O=Canonical Ltd., CN=Canonical Ltd. Master Certificate Authority
        ... (resto de la clave de Canonical) ...
[key 2]
SHA1 Fingerprint: 99:16:00:30:4c:d7:4b:4f:81:34:3b:4a:0a:ae:79:d5:3c:0c:88:5a
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            60:3e:f6:4e:02:14:96:c8:37:7d:af:71:89:16:0d:00:3c:38:85:59
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN=Mi Modulo Kernel Key
        Validity
            Not Before: May 24 20:28:00 2025 GMT  <-- (Importante: mencionar la corrección de esta fecha si la hiciste)
            Not After : Apr 30 20:28:00 2125 GMT
        Subject: CN=Mi Modulo Kernel Key
        
```

### Fase 3: Firma del Módulo del Kernel

Con la clave pública registrada y de confianza para el sistema, se procedió a firmar el módulo `mimodulo.ko`.
Primero, se aseguró que el módulo estuviera compilado con la última versión del código:

```
cd /home/tomy/kenel-modules/part1/module/
make clean
make
```

Luego, se utilizó el `script sign-file` (ubicado en `/usr/src/linux-headers-$(uname -r)/scripts/sign-file`) junto con la clave privada (`signing_key.priv`) y el certificado público (`signing_key.der`) para firmar el módulo `mimodulo.ko`.

```
sudo /usr/src/linux-headers-$(uname -r)/scripts/sign-file \
    sha512 \
    /home/tomy/module_signing_keys/signing_key.priv \
    /home/tomy/module_signing_keys/signing_key.der \
    /home/tomy/kenel-modules/part1/module/mimodulo.ko
```

El comando se ejecutó sin errores, indicando que el módulo fue firmado.
### Fase 4: Prueba del Módulo Firmado

Finalmente, se intentó cargar el módulo recién firmado en el kernel:

```
sudo insmod /home/tomy/kenel-modules/part1/module/mimodulo.ko
```

Para verificar el resultado, se examinaron los mensajes del kernel con `dmesg | tail -n 20`:

```
dmesg | tail -n 20
[    8.162771] wlp8s0: authenticate with 68:e2:09:eb:6e:50 (local address=d0:39:57:23:23:41)
[    8.162778] wlp8s0: send auth to 68:e2:09:eb:6e:50 (try 1/3)
[    8.166898] wlp8s0: authenticated
[    8.167647] wlp8s0: associate with 68:e2:09:eb:6e:50 (try 1/3)
[    8.183047] wlp8s0: RX AssocResp from 68:e2:09:eb:6e:50 (capab=0x1011 status=0 aid=1)
[    8.299470] wlp8s0: associated
[    8.299674] wlp8s0: Limiting TX power to 30 (30 - 0) dBm as advertised by 68:e2:09:eb:6e:50
[   12.729650] fbcon: Taking over console
[   12.737477] Console: switching to colour frame buffer device 240x67
[   12.998526] Lockdown: Xorg: raw io port access is restricted; see man kernel_lockdown.7
[   14.547524] Bluetooth: RFCOMM TTY layer initialized
[   14.547542] Bluetooth: RFCOMM socket layer initialized
[   14.547550] Bluetooth: RFCOMM ver 1.11
[   14.736999] Lockdown: systemd-logind: hibernation is restricted; see man kernel_lockdown.7
[   14.746650] Lockdown: systemd-logind: hibernation is restricted; see man kernel_lockdown.7
[   20.170539] systemd-journald[372]: /var/log/journal/b6bd465c0c044aaf9c0139ef9554d35c/user-1000.journal: Journal file uses a different sequence number ID, rotating.
[   32.690413] systemd-journald[372]: Time jumped backwards, rotating.
[  159.483402] warning: `ThreadPoolForeg' uses wireless extensions which will stop working for Wi-Fi 7 hardware; use nl80211
[  772.957700] mimodulo: loading out-of-tree module taints kernel.
[  772.959180] Modulo cargado en el kernel.
```

### Conclusión y Comparación

Antes de firmar el módulo y registrar la MOK, al intentar cargar mimodulo.ko en un sistema con Secure Boot activo, dmesg mostraba el siguiente error:

```
[timestamp] mimodulo: module verification failed: signature and/or required key missing - tainting kernel
```

Después de completar el proceso de firma y registro de la MOK, como se observa en la última salida de dmesg, el mensaje "module verification failed" ya no aparece. El módulo mimodulo se carga, y el único mensaje relacionado es "loading out-of-tree module taints kernel", lo cual es esperado para módulos externos y no indica un fallo de firma.

Esto demuestra que el proceso de firma del módulo del kernel fue exitoso y que el sistema, gracias a la MOK inscrita, ahora verifica y confía en la firma de nuestro módulo, permitiendo su carga en un entorno con Secure Boot habilitado.

## 9) Evidencia de compilación, carga y descarga del módulo
 
Modificamos el codigo dado de la siguiente manera:

```
#include <linux/module.h>   /* Requerido por todos los módulos */
#include <linux/kernel.h>   /* Definición de KERN_INFO */
#include <linux/init.h>     /* Para __init y __exit (buena práctica) */
#include <linux/utsname.h>  /* Para utsname() y struct new_utsname */

MODULE_LICENSE("GPL");      /* Licencia del modulo */
MODULE_DESCRIPTION("Modulo ejemplo que imprime el hostname"); // Descripción actualizada
MODULE_AUTHOR("Catedra de SdeC (Modificado por Tomy)");   // Puedes añadir tu nombre

// Prototipos (buena práctica para evitar warnings -Wmissing-prototypes)
static int __init modulo_lin_init(void);
static void __exit modulo_lin_clean(void);

/* Función que se invoca cuando se carga el módulo en el kernel */
static int __init modulo_lin_init(void) // Añadido static y __init
{
    struct new_utsname *uts = utsname(); // Obtener la estructura utsname

    // Imprimir el mensaje original y el nuevo mensaje con el hostname
    printk(KERN_INFO "Modulo LIN: Originalmente cargado en el kernel.\n");
    printk(KERN_INFO "Modulo LIN: Cargado en el equipo '%s'.\n", uts->nodename);

    /* Devolver 0 para indicar una carga correcta del módulo */
    return 0;
}

/* Función que se invoca cuando se descarga el módulo del kernel */
static void __exit modulo_lin_clean(void) // Añadido static y __exit
{
    struct new_utsname *uts = utsname(); // Obtener la estructura utsname

    // Imprimir el mensaje original y el nuevo mensaje con el hostname
    printk(KERN_INFO "Modulo LIN: Originalmente descargado del kernel.\n");
    printk(KERN_INFO "Modulo LIN: Descargado del equipo '%s'.\n", uts->nodename);
}

/* Declaración de funciones init y exit */
module_init(modulo_lin_init);
module_exit(modulo_lin_clean);
```

Luego realizamos un `make clean` y un `make` para ejecutar el codigo.

Obtuvimos el siguiente resultado:

```
make -C /lib/modules/6.8.0-60-generic/build M=/home/tomy/kenel-modules/part1/module modules
make[1]: se entra en el directorio '/usr/src/linux-headers-6.8.0-60-generic'
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: x86_64-linux-gnu-gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
  You are using:           gcc-13 (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0
  CC [M]  /home/tomy/kenel-modules/part1/module/mimodulo.o
  MODPOST /home/tomy/kenel-modules/part1/module/Module.symvers
  CC [M]  /home/tomy/kenel-modules/part1/module/mimodulo.mod.o
  LD [M]  /home/tomy/kenel-modules/part1/module/mimodulo.ko
  BTF [M] /home/tomy/kenel-modules/part1/module/mimodulo.ko
Skipping BTF generation for /home/tomy/kenel-modules/part1/module/mimodulo.ko due to unavailability of vmlinux
make[1]: se sale del directorio '/usr/src/linux-headers-6.8.0-60-generic'
```

Luego de esto re-firmamos el modulo usando:

```
sudo /usr/src/linux-headers-$(uname -r)/scripts/sign-file \
    sha512 \
    /home/tomy/module_signing_keys/signing_key.priv \
    /home/tomy/module_signing_keys/signing_key.der \
    /home/tomy/kenel-modules/part1/module/mimodulo.ko
```

Hecho esto lo cargamos:

```
sudo insmod /home/tomy/kenel-modules/part1/module/mimodulo.ko
```

Una vez cargado, revisamos con `dmesg` y obtenemos lo siguiente:

```
[  772.957700] mimodulo: loading out-of-tree module taints kernel.
[  772.959180] Modulo cargado en el kernel.
[ 2561.253509] Modulo descargado del kernel.
[ 2583.681825] Modulo LIN: Originalmente cargado en el kernel.
[ 2583.681844] Modulo LIN: Cargado en el equipo 'tomy'.
```

Vemos que obtenemos el resultado deseado

## 10) ¿Qué pasa si mi compañero con Secure Boot habilitado intenta cargar un módulo firmado por mí?

En un sistema con Secure Boot habilitado, si se intenta cargar un módulo del kernel firmado digitalmente por un tercero utilizando su propia clave MOK (Machine Owner Key) personal, la carga del módulo fallará.

Esto se debe a que el mecanismo de Secure Boot, a través del firmware UEFI y el kernel, verifica la firma digital del módulo contra una base de datos de claves públicas de confianza. Si el módulo fue firmado con una clave MOK cuya clave pública correspondiente está registrada únicamente en la lista MOK del sistema del firmante original, el sistema del compañero no poseerá esta clave pública específica en su propia lista MOK ni en la base de datos de claves de confianza de UEFI.

Consecuentemente, el sistema del compañero no podrá validar la autenticidad de la firma del módulo. Como resultado, el kernel rechazará la carga del módulo para mantener la integridad de la cadena de confianza de Secure Boot. Es probable que se registre un error en los logs del sistema (e.g., dmesg) indicando un fallo en la verificación de la firma o la ausencia de una clave requerida. Para que la carga sea exitosa, la clave pública del firmante original debería ser importada y registrada en la lista MOK del sistema del compañero.

## 11) Consecuencias del parche de Microsoft sobre GRUB (agosto 2024)
### a. ¿Cuál fue la consecuencia principal del parche de Microsoft sobre GRUB en sistemas con arranque dual (Linux y Windows)?

La consecuencia principal del parche de Microsoft, que actualizó la SBAT (Secure Boot Advanced Targeting) para revocar componentes del cargador de arranque GRUB asociados con la vulnerabilidad CVE-2022-2601, fue que los dispositivos configurados para arranque dual (Windows y Linux) ya no pudieron arrancar en sus sistemas Linux cuando Secure Boot estaba habilitado. Según el artículo, los usuarios afectados recibían el mensaje de error: "Verifying shim SBAT data failed: Security Policy Violation. Something has gone seriously wrong: SBAT self-check failed: Security Policy Violation." Este problema se presentó a pesar de que el boletín inicial de Microsoft indicaba que los sistemas de arranque dual no se verían afectados, impactando a múltiples distribuciones de Linux, incluidas versiones recientes como Ubuntu 24.04 y Debian 12.6.0.

### b. ¿Qué implicancia tiene desactivar Secure Boot como solución al problema descrito en el artículo?

El artículo menciona que desactivar Secure Boot en la configuración del firmware UEFI es una opción para que los usuarios afectados puedan volver a arrancar sus sistemas Linux. Al hacerlo, el firmware omite la verificación de la firma del cargador de arranque GRUB, permitiendo su ejecución incluso si su firma fue invalidada por la actualización de la SBAT.

La implicancia principal de esta solución es una disminución en la seguridad del sistema durante el proceso de arranque. El artículo indica que "Dependiendo de las necesidades de seguridad del usuario, esa opción puede no ser aceptable". Secure Boot está diseñado para prevenir la ejecución de firmware o software malicioso durante el arranque. Al desactivarlo, se elimina esta capa de protección, lo que significa que el sistema quedaría vulnerable a los mismos tipos de ataques (como los que explotan CVE-2022-2601) que Secure Boot y el parche de Microsoft intentaban prevenir.

### c. ¿Cuál es el propósito principal del Secure Boot en el proceso de arranque de un sistema?"

De acuerdo con el artículo, el propósito principal de Secure Boot es ser "el estándar de la industria para asegurar que los dispositivos que ejecutan Windows u otros sistemas operativos no carguen firmware o software malicioso durante el proceso de arranque". Su función es garantizar la integridad y autenticidad de cada componente de software cargado en la cadena de arranque, desde el firmware hasta el sistema operativo, mediante la verificación de firmas digitales. Esto tiene como objetivo proteger el sistema contra malware de bajo nivel, como bootkits y rootkits, que intentan comprometer el sistema antes de que las defensas del sistema operativo estén completamente activas.


# Conclusión
A lo largo del desarrollo del Trabajo Práctico N°4 se abordaron en profundidad múltiples aspectos fundamentales del funcionamiento del kernel de Linux, su interacción con los programas en espacio de usuario y las medidas de seguridad modernas implementadas a través de tecnologías como Secure Boot. La experiencia permitió al grupo no solo comprender conceptualmente la diferencia entre programas y módulos del kernel, sino también experimentar de forma práctica con la compilación, carga, descarga y firma digital de módulos propios.

En particular, se exploraron herramientas esenciales como modinfo, lsmod, strace, y hwinfo, que resultaron clave para la inspección del estado del sistema y la verificación de la interacción entre el software y el hardware. La firma digital del módulo con claves personalizadas, su inscripción mediante MOK, y la posterior carga exitosa en un entorno con Secure Boot activo, constituyeron una validación técnica importante, tanto por el aprendizaje adquirido como por el cumplimiento de requisitos de seguridad exigentes en sistemas actuales.

Además, se investigaron y documentaron a fondo los riesgos y desafíos asociados a la ejecución de código en el espacio del kernel, como los segmentation faults, el manejo de señales y la gestión de errores críticos. También se analizó el impacto de actualizaciones de seguridad recientes, como el parche de Microsoft sobre GRUB, lo cual evidenció la importancia de comprender las implicancias de la cadena de confianza y cómo puede verse interrumpida en configuraciones de arranque dual.

En síntesis, este trabajo integró conocimientos teóricos y prácticos en un contexto realista, fortaleciendo la comprensión del modo protegido, el entorno de ejecución del kernel, la seguridad del proceso de arranque y la responsabilidad que implica desarrollar software que opera a tan bajo nivel. El grupo considera cumplidos con éxito los objetivos propuestos, habiendo adquirido habilidades que serán de gran valor en el desarrollo de sistemas seguros y robustos.