global multiplicar
section .text

multiplicar:
    ; xmm0 = a, xmm1 = b
    mulss xmm0, xmm1
    ret
