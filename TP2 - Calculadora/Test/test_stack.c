#include <stdio.h>

// Declaramos la función que está en ASM
extern int sumar_uno(int x);

int main() {
    int valor = 41;
    int resultado;

    printf("Antes de llamar a sumar_uno:\n");
    printf("valor = %d\n", valor);

    resultado = sumar_uno(valor);

    printf("Después de llamar a sumar_uno:\n");
    printf("resultado = %d\n", resultado);

    return 0;
}