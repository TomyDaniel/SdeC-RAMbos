#include <stdio.h>

// Declarar la función ASM que SÍ vamos a probar
extern int procesar_gini_asm(float valor_gini);

int main() {
    float test_float = 42.8; // Valor de prueba
    int resultado_int;

    printf("C: Valor float a enviar: %f\n", test_float);
    // Breakpoint ANTES
    resultado_int = procesar_gini_asm(test_float);
    // Breakpoint DESPUÉS
    printf("C: Valor int recibido: %d\n", resultado_int); // Debería ser 42 + 1 = 43

    return 0;
    // Breakpoint DENTRO (en procesar_gini_asm)
}