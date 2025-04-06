; sumar_uno.asm – versión x86_64
global sumar_uno
section .text

sumar_uno:
    ; Parámetro está en xmm0 (ABI x86_64 para float)
    ; Sumamos 1.0f usando instrucciones SSE

    movss xmm1, dword [rel uno]
    addss xmm0, xmm1      ; xmm0 = xmm0 + 1.0f
    ret

section .data
uno: dd 1.0
