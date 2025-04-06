global promedio
section .text

promedio:
    ; a está en xmm0, b está en xmm1 (ABI de x86_64)
    ; resultado final en xmm0

    addss xmm0, xmm1       ; xmm0 = a + b
    movss xmm2, dword [rel divisor]
    divss xmm0, xmm2       ; xmm0 = (a + b) / 2
    ret

section .data
divisor: dd 2.0
