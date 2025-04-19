// libgini_wrapper.c
extern float sumar_uno(float valor);
extern float promedio(float a, float b);
extern float multiplicar(float a, float b);
extern float dividir(float a, float b);
extern int procesar_gini_asm(float valor_gini);

int procesar_gini_final(float valor_gini) {
    return procesar_gini_asm(valor_gini);
}