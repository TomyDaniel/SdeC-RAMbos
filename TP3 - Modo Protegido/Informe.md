# Informe del Proyecto TP3: Modo Protegido

**Grupo/Autor:** *Rambos*  
**Materia:** Sistemas de Computación  
**Alumnos:**
- Viale, Sofia
- Daniel, Tomas G  

**Docentes:**
- Solinas, Miguel A.
- Jorge, Javier

## Respuestas Linker

# Respuestas sobre Linkers y Proceso de Enlazado

## 1. ¿Qué es un linker? ¿Qué hace?

*   **¿Qué es?**
    Un **linker** (enlazador) es una herramienta de desarrollo de software fundamental. Es un programa que toma uno o más *ficheros objeto* (generados por un compilador o ensamblador) y los combina para crear un único fichero ejecutable, una biblioteca (compartida o estática) u otro fichero objeto.

*   **¿Qué hace?**
    Las tareas principales de un linker son:
    1.  **Resolución de Símbolos:** Durante la compilación, si un fichero fuente hace referencia a una variable o función definida en otro fichero (o en una biblioteca), el compilador deja una referencia "pendiente" o "externa". El linker busca dónde están definidos estos símbolos (funciones, variables globales) en todos los ficheros objeto y bibliotecas de entrada y reemplaza las referencias pendientes con las direcciones de memoria correctas.
    2.  **Relocalización (Relocation):** Los ficheros objeto suelen contener código y datos con direcciones relativas o basadas en cero. El linker asigna direcciones de memoria finales y absolutas a las distintas secciones de código y datos (como `.text`, `.data`, `.bss`). Luego, ajusta las referencias a código y datos dentro del programa para que apunten a estas direcciones finales.
    3.  **Combinación de Secciones:** Combina secciones similares de los diferentes ficheros objeto de entrada (por ejemplo, todos los `.text` se juntan en una única sección `.text` en el fichero de salida, lo mismo para `.data`, etc.).
    4.  **Enlazado con Bibliotecas:** Si el programa utiliza funciones de bibliotecas (estáticas `.a` o dinámicas `.so`/`.dll`), el linker incorpora el código necesario de las bibliotecas estáticas o añade referencias para que el cargador del sistema operativo pueda cargar las bibliotecas dinámicas en tiempo de ejecución.

## 2. ¿Qué es la dirección que aparece en el script del linker? ¿Por qué es necesaria?

*   **¿Qué es?**
    La dirección que aparece en un *linker script* (guion del enlazador) es típicamente la **dirección de carga (Load Address - LMA)** o la **dirección virtual (Virtual Address - VMA)** base para el programa o para secciones específicas del mismo. Indica dónde se espera que el código y los datos residan en la memoria cuando el programa se ejecute.
    *   **VMA (Virtual Memory Address):** La dirección donde el programa *espera* estar una vez cargado y ejecutándose. Es la dirección que usan las instrucciones y referencias dentro del programa.
    *   **LMA (Load Memory Address):** La dirección donde el programa (o una sección) debe ser *cargado* inicialmente por el cargador o bootloader. En sistemas simples o embebidos, VMA y LMA suelen ser iguales. En sistemas con MMU o que copian código de ROM a RAM, pueden diferir.

*   **¿Por qué es necesaria?**
    Esta dirección es crucial por varias razones:
    1.  **Determinación de Direcciones Absolutas:** Permite al linker calcular las direcciones absolutas finales para todas las funciones y variables globales. Sin una dirección base, el linker solo podría generar código relocalizable, pero no un ejecutable final listo para cargar en una dirección específica.
    2.  **Mapeo de Memoria:** Define cómo se organiza el programa en el espacio de direcciones de la máquina destino. Es fundamental en sistemas embebidos o *bare-metal* donde el programador debe controlar explícitamente dónde se ubica el código (p.ej., en Flash ROM) y los datos (p.ej., en RAM).
    3.  **Cargador/Bootloader:** Informa al cargador del sistema operativo o al bootloader dónde debe colocar las diferentes partes del programa en la memoria física o virtual antes de transferirle el control.
    4.  **Interacción con Hardware:** En sistemas embebidos, ciertas direcciones de memoria corresponden a registros de hardware o áreas específicas (como vectores de interrupción). El linker script asegura que el código o datos necesarios se coloquen en esas direcciones predefinidas.

## 3. Compare la salida de `objdump` con `hd`, verifique dónde fue colocado el programa dentro de la imagen.

Para realizar esta comparación, necesitarías un fichero ejecutable (por ejemplo, `mi_programa`) generado por un linker (posiblemente usando un linker script específico).

*   **`objdump`:** Es una utilidad para mostrar información contenida dentro de ficheros objeto o ejecutables.
    *   `objdump -h mi_programa`: Muestra las cabeceras de las secciones. Busca secciones como `.text` (código), `.data` (datos inicializados), `.bss` (datos no inicializados). Fíjate en las columnas `VMA`, `LMA` y `File off` (desplazamiento en el fichero). La VMA/LMA te dice la dirección de memoria *destino* y `File off` te dice *dónde* empieza esa sección dentro del propio fichero.
    *   `objdump -d mi_programa`: Desensambla la sección de código (`.text`). Muestra las instrucciones máquina junto con las direcciones de memoria (VMA) donde se ubicarán. La primera dirección que veas será la VMA de inicio de la sección `.text`.

*   **`hd` (o `hexdump`)**: Es una utilidad para mostrar el contenido de un fichero en formato hexadecimal (y opcionalmente ASCII).
    *   `hd mi_programa` o `hexdump -C mi_programa`: Muestra los bytes crudos del fichero. La primera columna suele ser el desplazamiento (offset) dentro del fichero.

*   **Verificación:**
    1.  Ejecuta `objdump -h mi_programa` y anota el `File off` y la `VMA`/`LMA` de la sección `.text`.
    2.  Ejecuta `objdump -d mi_programa` y observa las primeras instrucciones y sus direcciones (VMA).
    3.  Ejecuta `hd mi_programa`. Busca en la salida de `hd` el desplazamiento (`offset`) que anotaste como `File off` de la sección `.text`.
    4.  Los bytes hexadecimales que muestra `hd` a partir de ese offset deben corresponder a los bytes de las instrucciones máquina que muestra `objdump -d` al inicio de la sección `.text`.
    5.  **Conclusión:** `objdump` te dice dónde *debería* estar el programa en memoria (VMA/LMA) y dónde *está* guardado dentro del fichero (`File off`). `hd` te permite ver los bytes *reales* guardados en esa posición (`File off`) dentro del fichero. Comparando ambas salidas en el `File off` correcto, confirmas que el código correspondiente a la VMA/LMA está efectivamente almacenado en esa ubicación del fichero imagen.

## 4. Grabar la imagen en un pendrive y probarla en una PC y subir una foto.

Este paso es práctico y depende del tipo de imagen que hayas generado (¿es un bootloader, un kernel mínimo?).

*   **Proceso General:**
    1.  **Obtener la Imagen:** Asegúrate de tener el fichero imagen final (probablemente en formato binario crudo, ver pregunta 5). Llamémoslo `imagen.bin`.
    2.  **Identificar el Pendrive:** Conecta el pendrive a tu PC. Identifica cuidadosamente el nombre de dispositivo asignado por el sistema operativo (p.ej., `/dev/sdb`, `/dev/sdc` en Linux; `disk2`, `disk3` en macOS). **¡PRECAUCIÓN! Elegir el dispositivo incorrecto puede borrar datos importantes.** Herramientas como `lsblk` (Linux) o `diskutil list` (macOS) ayudan.
    3.  **Grabar la Imagen:** Usa una herramienta como `dd` (Linux/macOS) o Rufus/BalenaEtcher (multiplataforma).
        *   **Con `dd` (ejemplo para Linux, ¡CON MUCHO CUIDADO!):**
            ```bash
            sudo dd if=imagen.bin of=/dev/sdX bs=4M status=progress conv=fsync
            ```
            Reemplaza `imagen.bin` con el nombre de tu fichero y `/dev/sdX` con el dispositivo *correcto* de tu pendrive (¡NO la partición como `/dev/sdX1`!). `bs=4M` establece un tamaño de bloque razonable, `status=progress` muestra el progreso, y `conv=fsync` asegura que los datos se escriban físicamente antes de que el comando termine.
    4.  **Expulsar de Forma Segura:** Desmonta y expulsa el pendrive correctamente.
    5.  **Probar en la PC:**
        *   Reinicia la PC donde quieres probar la imagen.
        *   Entra en la configuración de la BIOS/UEFI (usualmente presionando F2, F10, F12, DEL o ESC durante el arranque).
        *   Configura el orden de arranque (Boot Order) para que arranque primero desde el dispositivo USB.
        *   Guarda los cambios y reinicia.
    6.  **Observar y Capturar:** Si todo funciona, la PC debería intentar arrancar desde el pendrive y ejecutar tu imagen. Verás lo que sea que tu programa haga (imprimir un mensaje, parpadear el cursor, etc.). Toma una foto de la pantalla mostrando el resultado.

*   **Subir la Foto:** (Instrucción para ti) Deberás subir el archivo de imagen (la foto) a través de la plataforma o método que estés utilizando para entregar este documento. Markdown en sí no puede incrustar directamente una imagen que subas en el momento, pero puedes incluir una referencia si la subes a algún sitio: `![Foto de la prueba](URL_de_la_imagen)` o simplemente mencionar que la foto se adjunta por separado.

## 5. ¿Para qué se utiliza la opción `--oformat binary` en el linker?

La opción `--oformat binary` (o su forma corta `-O binary`) le indica al linker (`ld` u otro compatible) que genere el fichero de salida en formato **binario crudo (raw binary)** en lugar de un formato de fichero objeto estándar como ELF, COFF, o Mach-O.

*   **Características del formato binario crudo:**
    *   No contiene metadatos: Elimina toda la información extra como cabeceras de fichero (p.ej., cabecera ELF), tablas de secciones, tablas de símbolos, información de relocalización o depuración.
    *   Contenido directo: El fichero resultante contiene únicamente los bytes de las secciones que se marcan como "cargables" (normalmente `.text`, `.data`, etc.), concatenadas en el orden y con los rellenos (padding) especificados (o implícitos) por el linker script o las opciones del linker.
    *   Imagen de memoria: Esencialmente, es una imagen directa de cómo se supone que esas secciones deben aparecer en memoria a partir de la dirección de carga (LMA).

*   **Usos principales:**
    1.  **Bootloaders:** Muchos bootloaders de primera o segunda etapa deben ser imágenes binarias crudas porque el hardware o el firmware que los carga no entiende formatos complejos como ELF. Simplemente copia los bytes del fichero directamente a una dirección de memoria específica y salta a ella.
    2.  **Firmware para Sistemas Embebidos/Microcontroladores:** Al programar la memoria Flash/ROM de un microcontrolador, a menudo se necesita un fichero binario que represente exactamente los bytes a escribir en la memoria.
    3.  **Imágenes de Kernel (casos específicos):** Algunos bootloaders esperan cargar la imagen inicial del kernel del sistema operativo como un fichero binario crudo.
    4.  **Creación de ROMs:** Para emuladores o programadores de EPROM/Flash.

En resumen, se usa cuando se necesita una representación pura del código y datos tal como deben residir en memoria, sin la sobrecarga o estructura de los formatos de fichero ejecutables estándar. Es ideal para cargar directamente en memoria o para grabar en dispositivos de almacenamiento no volátil que no interpretan formatos de fichero complejos.

# Respuestas sobre Modo Protegido x86 y Segmentación

## 1. Crear un código assembler que pueda pasar a modo protegido (sin macros).

Para pasar de Modo Real a Modo Protegido, se deben seguir estos pasos fundamentales:

1.  **Deshabilitar Interrupciones:** Para evitar interrupciones durante la transición crítica.
2.  **Cargar la GDT (Global Descriptor Table):** Usar la instrucción `lgdt` para decirle al procesador dónde está la tabla de descriptores de segmento.
3.  **Habilitar el Modo Protegido:** Poner a 1 el bit PE (Protection Enable, bit 0) del registro de control `CR0`.
4.  **Salto Lejano (Far Jump):** Realizar un `jmp` a una dirección de código ya en modo protegido. Esto es crucial para:
    *   Limpiar la cola de prefetch de instrucciones del modo real.
    *   Cargar el registro `CS` con un selector válido de la GDT que apunte a un descriptor de segmento de código de 32 bits.

Aquí tienes un ejemplo básico usando NASM (Netwide Assembler):

```asm
bits 16         ; Ensamblamos inicialmente en modo real de 16 bits
org 0x1000      ; Dirección de carga asumida

start:
    cli           ; 1. Deshabilitar interrupciones

    ; 2. Configurar y cargar la GDT
    lgdt [gdt_ptr] ; Cargar el registro GDTR con la dirección y límite de nuestra GDT

    ; 3. Habilitar modo protegido (bit 0 de CR0)
    mov eax, cr0  ; Leer el registro de control CR0
    or eax, 1     ; Poner el bit 0 (Protection Enable - PE) a 1
    mov cr0, eax  ; Escribir el valor modificado de vuelta a CR0

    ; 4. Salto largo (far jump) para limpiar la cola de prefetch y cargar CS
    ;    CS ahora apuntará al descriptor CODE_SEG (offset 8 en la GDT)
    jmp CODE_SEG:protected_mode

; --- Fin del código de 16 bits ---

bits 32         ; A partir de aquí, estamos en modo protegido de 32 bits
protected_mode:
    ; 5. Cargar los otros registros de segmento (DS, SS, ES, etc.)
    ;    con el selector del segmento de datos (offset 16 en la GDT)
    mov ax, DATA_SEG
    mov ds, ax
    mov ss, ax
    mov es, ax
    mov fs, ax
    mov gs, ax

    ; 6. Configurar la pila (Stack Pointer)
    mov esp, stack_top

    ; --- Aquí comienza el código en modo protegido ---
    ; Ejemplo: Escribir un caracter en la memoria de video (esquina superior izq)
    mov edi, 0xb8000         ; Dirección de memoria de video en modo texto
    mov ah, 0x0F            ; Atributo: Blanco sobre negro
    mov al, 'P'
    mov [edi], ax           ; Escribir 'P'
    add edi, 2
    mov al, 'M'
    mov [edi], ax           ; Escribir 'M'

    ; Bucle infinito para detener la ejecución
halt_loop:
    hlt
    jmp halt_loop

; --- Datos y Definiciones ---

; GDTR Pointer Structure
gdt_ptr:
    dw gdt_end - gdt_start - 1 ; Límite de la GDT (tamaño - 1)
    dd gdt_start               ; Dirección base lineal de la GDT

; Global Descriptor Table (GDT)
gdt_start:
; Descriptor NULO (obligatorio)
gdt_null:
    dq 0x0000000000000000    ; Define 8 bytes (64 bits) como 0

; Descriptor de Segmento de Código (CODE_SEG) - Selector 0x08
gdt_code:
    ; Limit (bits 0-15), Base (bits 0-15)
    dw 0xFFFF
    dw 0x0000
    ; Base (bits 16-23)
    db 0x00
    ; Access Byte: Present(1), DPL=0(00), Type=Code(1), Executable(1), Dir/Conf(0), Readable(1), Accessed(0) -> 1001 1010b = 0x9A
    db 0x9A
    ; Flags(bits 4-7) + Limit(bits 16-19): Granularity=4K(1), 32-bit(1), Long=0(0), AVL=0(0) -> 1100b, Limit=1111b -> 1100 1111b = 0xCF
    db 0xCF
    ; Base (bits 24-31)
    db 0x00

; Descriptor de Segmento de Datos (DATA_SEG) - Selector 0x10
gdt_data:
    ; Limit (bits 0-15), Base (bits 0-15)
    dw 0xFFFF
    dw 0x0000
    ; Base (bits 16-23)
    db 0x00
    ; Access Byte: Present(1), DPL=0(00), Type=Data(1), ExpandDown=0(0), Writable(1), Accessed(0) -> 1001 0010b = 0x92
    db 0x92
    ; Flags(bits 4-7) + Limit(bits 16-19): Granularity=4K(1), 32-bit(1), Long=0(0), AVL=0(0) -> 1100b, Limit=1111b -> 1100 1111b = 0xCF
    db 0xCF
    ; Base (bits 24-31)
    db 0x00

gdt_end:

; Selectores (Offsets desde gdt_start)
CODE_SEG equ gdt_code - gdt_start
DATA_SEG equ gdt_data - gdt_start

; Pila (Stack)
stack_bottom:
    resb 4096 * 4           ; Reservar 16KB para la pila
stack_top:                  ; Etiqueta para la cima de la pila (esp apunta aquí)
```

**Compilación (ejemplo con NASM):**
```
nasm -f bin protected_mode.asm -o protected_mode.bin
```

## 2. ¿Cómo sería un programa que tenga dos descriptores de memoria diferentes, uno para cada segmento (código y datos) en espacios de memoria diferenciados?

Para lograr esto, simplemente necesitas definir bases diferentes en los descriptores de la GDT para los segmentos de código y datos. El hardware (la MMU, aunque aquí aún no usemos paginación) añadirá la base del descriptor a la dirección lógica usada en la instrucción para obtener la dirección lineal.
Modificamos la GDT del ejemplo anterior:

```
bits 16         ; Empezamos en Modo Real (16 bits)
org 0x7C00      ; Dirección típica de carga para un sector de arranque

start:
    cli             ; 1. Deshabilitar interrupciones

    ; Cargar el puntero a la GDT
    lgdt [gdt_ptr]  ; 2. Cargar registro GDTR

    ; 3. Habilitar Modo Protegido (poner bit 0 de CR0 a 1)
    mov eax, cr0    ; Leer CR0
    or  eax, 0x1    ; Poner el bit PE (Protection Enable)
    mov cr0, eax    ; Escribir de vuelta a CR0

    ; 4. Salto lejano para cargar CS y limpiar la cola de instrucciones
    ; El selector 0x08 apunta al segundo descriptor en nuestra GDT (el de código)
    ; pmode_entry es la etiqueta donde comienza el código de 32 bits
    jmp 0x08:pmode_entry

; --- Tabla de Descriptores Globales (GDT) ---
gdt_start:
    ; Descriptor Nulo (Obligatorio)
    dq 0x0000000000000000

    ; Descriptor de Segmento de Código (CS)
    ; BASE = 0x00010000, Limite=4GB (o más específico), Ring 0, Exec/Read
    dw 0xFFFF       ; Límite (0-15) - Simplificado a 4GB
    dw 0x0000       ; Base (0-15)  -> de 0x00010000
    db 0x01         ; Base (16-23) -> de 0x00010000
    db 0x9A         ; Access: P=1, DPL=00, S=1, Type=Code, E=1, C=0, R=1, A=0
    db 0xCF         ; Flags(G=1,D=1) + Limit(19:16)
    db 0x00         ; Base (24-31) -> de 0x00010000

    ; Descriptor de Segmento de Datos (DS, ES, FS, GS, SS)
    ; BASE = 0x00080000, Limite=4GB (o más específico), Ring 0, Data, Read/Write
    dw 0xFFFF       ; Límite (0-15) - Simplificado a 4GB
    dw 0x0000       ; Base (0-15)  -> de 0x00080000
    db 0x08         ; Base (16-23) -> de 0x00080000
    db 0x92         ; Access: P=1, DPL=00, S=1, Type=Data, E=0, ED=0, W=1, A=0
    db 0xCF         ; Flags(G=1,D=1) + Limit(19:16)
    db 0x00         ; Base (24-31) -> de 0x00080000

gdt_end:

; ... (Puntero GDT igual) ...

; --- Código de Modo Protegido (32 bits) ---
bits 32
pmode_entry:
    ; Estamos en PM. CS apunta al descriptor con base 0x10000
    ; Cargar DS, etc., con el selector del descriptor de datos (0x10) con base 0x80000
    mov ax, 0x10
    mov ds, ax
    mov ss, ax ; La pila también usará la base 0x80000
    ; mov es, ax ... etc.

    ; EJEMPLO:
    ; Si este código está físicamente en 0x10000 + offset_codigo
    ; Y queremos escribir en una variable 'my_var' que está físicamente en 0x80000 + offset_datos

    ; Suponiendo que 'my_var' está definida en la sección de datos que el enlazador
    ; (o nosotros manualmente) colocaría a partir de 0x80000

    ; mov dword [my_var_logical_offset], 1234h ; El procesador calculará:
                                             ; Dirección Lineal = Base DS (0x80000) + my_var_logical_offset

    ; Escribir en pantalla (usa dirección física fija, no afectada por DS)
    mov edi, 0xb8000
    mov ah, 0x0A ; Verde sobre negro
    mov al, 'D'
    mov [edi], ax

    hlt

; --- Datos (ASUMIENDO que un cargador los pondría en 0x80000) ---
; ¡ESTA PARTE ES MÁS CONCEPTUAL EN ESTE SIMPLE EJEMPLO!
; Un enlazador/cargador real se encargaría de colocar los datos
; en la dirección física 0x80000.
; data_section_start_physical equ 0x80000
; my_var_logical_offset equ 0 ; O el offset relativo al inicio de datos
; ; En la ubicación física 0x80000 iría:
; ; my_var dd 0

; --- Datos ---
bits 16             ; Volver a 16 bits para los datos que se cargan en modo real
msg_ok db 'OK PM', 0

; Rellenar hasta 510 bytes y añadir firma de sector de arranque
times 510 - ($-$$) db 0
dw 0xAA55
```

**Importante:** En este ejemplo simple sin un enlazador sofisticado o cargador, asegurar que el código realmente termine en 0x10000 y los datos en 0x80000 requeriría pasos adicionales (por ejemplo, usando org cuidadosamente o un formato de salida y un cargador que respete las direcciones). El punto clave es que los descriptores le dicen al CPU dónde esperar que estén esos segmentos.

## 3. Cambiar los bits de acceso del segmento de datos para que sea de solo lectura, intentar escribir, ¿Qué sucede? ¿Qué debería suceder a continuación? Verificarlo con GDB.

- **Cambiar el Descriptor:**
Modificamos el byte de acceso del descriptor de datos. El bit de Escritura (W) es el bit 1 del campo 'Type' para descriptores de datos.  
    - Descriptor R/W (Read/Write): 10010010b (0x92) -> P=1, DPL=00, S=1, Type=Data(E=0,ED=0,W=1,A=0)  
    - Descriptor RO (Read-Only): 10010000b (0x90) -> P=1, DPL=00, S=1, Type=Data(E=0,ED=0,W=0,A=0)  

Reemplaza db 0x92 por db 0x90 en la definición del descriptor de datos en la GDT del ejemplo.

- **Intentar Escribir:**  
Añade una instrucción en el código de modo protegido que intente escribir en memoria usando un registro de segmento cargado con el selector del descriptor de datos (0x10).

```
bits 32
pmode_entry:
    mov ax, 0x10    ; Selector de datos (Ahora RO)
    mov ds, ax
    mov ss, ax      ; La pila también es RO si usa este selector! Cuidado.
    ; ... otros segmentos si es necesario

    ; Intento de escritura ILEGAL
    mov dword [0x1000], 0xDEADBEEF  ; Escribir en offset 0x1000 relativo a la base de DS

    ; Si llegamos aquí, algo falló en la protección (no debería)
    mov edi, 0xb8000
    mov dword [edi], 0x0C4E4F0A ; 'NO' en Rojo

    hlt
```

- **¿Qué sucede?**  
Cuando la CPU ejecuta mov dword [0x1000], 0xDEADBEEF, realiza las siguientes comprobaciones (entre otras):  
    - Consulta el descriptor asociado al selector en DS (el 0x10).  
    - Verifica los permisos en el byte de acceso (0x90).  
    - Detecta que el bit de Escritura (W) está a 0, pero la operación es una escritura.  
    - ¡Esto es una violación de protección!  
- **¿Qué debería suceder a continuación?**  
La CPU debería generar una **Excepción de Fallo de Protección General (#GP)**. Este es el vector de interrupción número 13 (0x0D).
Al generar la excepción #GP:  
    - La CPU busca en la IDT (Interrupt Descriptor Table) la entrada correspondiente al vector 13.
    - Si se encuentra un manejador de interrupción válido (y los permisos son correctos), la CPU empuja en la pila (la que define SS, que podría ser la RO también, ¡causando un Doble Fallo!):  
        - El selector del segmento que causó el fallo (si aplica, aquí es 0x10).  
        - EFLAGS.
        - CS:EIP de la instrucción que falló (mov dword [0x1000]...).  
    - Luego, salta a la dirección del manejador de interrupciones especificado en la IDT para #GP.
    - Si NO hay una IDT válida configurada, o si ocurre un error al intentar invocar al manejador de #GP (por ejemplo, intentar escribir en la pila de un segmento RO), la CPU genera un Doble Fallo (#DF).  
    - Si ocurre un error al intentar invocar al manejador de Doble Fallo, la CPU genera un Triple Fallo. Un triple fallo generalmente causa un reset del procesador.

En un código simple como este, donde no hemos configurado una IDT, lo más probable es que ocurra un Triple Fallo y el sistema (o emulador) se reinicie o se detenga abruptamente.

- **Verificarlo con GDB (usando QEMU):**
    -  **Ensamblar:** nasm -f bin protected_mode_ro.asm -o protected_mode_ro.bin
    - **Ejecutar con QEMU + GDB Server:**
    ```
    qemu-system-i386 -fda protected_mode_ro.bin -S -gdb tcp::1234
    ```

    - `-fda`: Carga el binario como disquete.
    - `-S`: Detiene la CPU al inicio (espera a GDB).
    - `-gdb tcp::1234`: Inicia un servidor GDB en el puerto 1234.

    - **Conectar GDB:**  
        - Abre otra terminal y ejecuta `gdb`.
        - Dentro de GDB: `target remote localhost:1234`.  
    
    - **Establecer arquitectura y modo:**
        - `set architecture i386`
    
    - **Poner Breakpoint:** Necesitas saber la dirección de la instrucción mov dword `[0x1000], 0xDEADBEEF`. Puedes desensamblar (`disassemble /m pmode_entry`) o calcularla. Supongamos que está en `0x7C00 + offset`. O más fácil, si la etiqueta `pmode_entry` está bien definida: `break pmode_entry` y luego usar `stepi` o `nexti` para avanzar hasta justo antes de la escritura. O break `*<direccion_del_mov>`

    ## 4. En modo protegido, ¿Con qué valor se cargan los registros de segmento? ¿Porqué?

*   **¿Con qué valor?**  
    En Modo Protegido, los registros de segmento (`CS`, `DS`, `ES`, `FS`, `GS`, `SS`) se cargan con un valor de 16 bits llamado **Selector**.

*   **¿Por qué?**  
    La razón fundamental es que en Modo Protegido, un segmento de memoria ya no se define simplemente por una dirección base (como en Modo Real, donde `Segmento * 16 = Base`), sino por un conjunto mucho más rico de atributos almacenados en un **Descriptor de Segmento** dentro de la GDT (o LDT).

    Un descriptor de segmento (8 bytes) contiene información vital como:
    1.  **Dirección Base (32 bits):** Dónde comienza el segmento en el espacio de direcciones lineales.
    2.  **Límite del Segmento (20 bits + flag G):** El tamaño del segmento (hasta 4GB con granularidad de 4KB, o 1MB con granularidad de byte).
    3.  **Tipo y Atributos (Byte de Acceso):**
        *   Si es un segmento de Código o Datos.
        *   Permisos (Lectura, Escritura, Ejecución).
        *   Nivel de Privilegio (DPL - Descriptor Privilege Level).
        *   Si el descriptor es válido (Bit Presente).
        *   Si es un segmento de sistema (para TSS, LDT, etc.).
    4.  **Flags:** Como la granularidad (G), tamaño por defecto de operando (D/B).

    Toda esta información (8 bytes) no cabe en un registro de segmento de 16 bits. Por lo tanto, en lugar de contener la información directamente, el registro de segmento contiene un **Selector**, que actúa como un índice o puntero hacia la entrada correcta (el Descriptor) en la GDT o LDT.

    La estructura de un Selector de 16 bits es:
    *   **Índice (Bits 15-3):** Especifica qué entrada usar en la GDT/LDT (multiplicado por 8 da el offset en bytes dentro de la tabla).
    *   **TI (Table Indicator, Bit 2):** Indica si se usa la GDT (0) o la LDT (1).
    *   **RPL (Requested Privilege Level, Bits 1-0):** El nivel de privilegio que solicita el código que carga el selector.

    Cuando se carga un selector en un registro de segmento (p.ej., `mov ds, ax`), la CPU realiza las siguientes acciones:
    1.  Usa el Índice y TI del selector para localizar el descriptor correspondiente en la GDT o LDT.
    2.  Realiza comprobaciones de protección (¿Es válido el selector? ¿Está presente el descriptor? ¿Son los permisos y privilegios adecuados para la operación?).
    3.  Si todo es correcto, carga la información del descriptor (Base, Límite, Atributos) en **registros internos ocultos (cache de descriptores)** asociados al registro de segmento visible (`DS` en este caso).
    4.  A partir de ese momento, cuando se use `DS` para acceder a memoria, la CPU utilizará la información cacheada (Base, Límite, Permisos) para calcular la dirección lineal y verificar los permisos, sin tener que volver a leer la GDT/LDT para cada acceso.

    Por lo tanto, el Selector es un mecanismo indirecto y eficiente para permitir que los registros de segmento de 16 bits controlen el acceso a segmentos de memoria definidos por descriptores mucho más grandes y complejos, implementando así las características de protección y segmentación del Modo Protegido.