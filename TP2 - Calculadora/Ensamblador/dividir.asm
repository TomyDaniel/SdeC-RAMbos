global dividir
section .text

dividir:
    ; xmm0 = a, xmm1 = b
    divss xmm0, xmm1
    ret
