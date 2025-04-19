; En un archivo como procesador_gini.asm
global procesar_gini_asm
section .text

procesar_gini_asm:
    push ebp
    mov ebp, esp

    ; Cargar el float desde la pila (pasado como argumento)
    fld dword [ebp + 8]

    ; Crear espacio en la pila para el entero resultante de la conversión
    sub esp, 4
    ; Convertir st0 a entero (usando modo de redondeo por defecto)
    ; y almacenarlo en la cima de la pila ([esp])
    ; fistp también elimina el valor de la pila FPU (st0)
    fistp dword [esp]

    ; Mover el entero desde la pila del sistema a EAX
    pop eax

    ; Sumar 1 al entero en EAX (requisito del TP)
    add eax, 1

    ; Restaurar puntero de pila y base
    mov esp, ebp  ; o leave si no hubo 'sub esp' significativo
    pop ebp
    ret           ; El resultado int está en EAX