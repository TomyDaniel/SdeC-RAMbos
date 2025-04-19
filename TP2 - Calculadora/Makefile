# Makefile para TP2

# Compilador y Ensamblador
CC = gcc
NASM = nasm
CFLAGS = -m32 -g3   # Flags para C (32 bits, debug)
NASMFLAGS = -f elf -g -F dwarf # Flags para NASM (32 bits ELF, debug)
LDFLAGS = -m32 -g3 -shared # Flags para el enlazador (32 bits, debug, shared lib)
LDFLAGS_EXEC = -m32 -g3    # Flags para enlazar ejecutables (32 bits, debug)

# Directorios
SRC_C_DIR = C
SRC_ASM_DIR = Ensamblador
OBJ_DIR = obj
BIN_DIR = .# Directorio de salida para .so y ejecutables
PYTHON_DIR = Python

# Archivos Fuente
C_SOURCES = $(wildcard $(SRC_C_DIR)/*.c)
ASM_SOURCES = $(wildcard $(SRC_ASM_DIR)/*.asm)

# Archivos Objeto (calculados a partir de las fuentes)
OBJ_C_WRAPPER = $(patsubst $(SRC_C_DIR)/%.c,$(OBJ_DIR)/%.o,$(filter %/libgini_wrapper.c, $(C_SOURCES)))
OBJ_ASM = $(patsubst $(SRC_ASM_DIR)/%.asm,$(OBJ_DIR)/%.o,$(ASM_SOURCES))
OBJ_TEST_C = $(patsubst $(SRC_C_DIR)/%.c,$(OBJ_DIR)/%.o,$(filter %/test_procesador.c, $(C_SOURCES)))
OBJ_ASM_PROCESS = $(filter $(OBJ_DIR)/procesar_gini.o, $(OBJ_ASM)) # Objeto ASM específico para el test

# Archivos de Salida
TARGET_LIB = $(BIN_DIR)/libgini.so
TARGET_TEST_DEBUG = $(BIN_DIR)/test_procesador_debug
PYTHON_CLIENT = $(PYTHON_DIR)/gini_cliente.py

# --- Reglas Principales ---

# Regla por defecto (lo que se ejecuta si solo escribes 'make')
all: $(TARGET_LIB) $(TARGET_TEST_DEBUG)

# Regla para crear la biblioteca compartida
$(TARGET_LIB): $(OBJ_C_WRAPPER) $(OBJ_ASM)
	@echo "==> Enlazando biblioteca compartida $@"
	$(CC) $(LDFLAGS) $^ -o $@
	@echo "==> Biblioteca $(TARGET_LIB) creada."

# Regla para crear el ejecutable de prueba para GDB
$(TARGET_TEST_DEBUG): $(OBJ_TEST_C) $(OBJ_ASM_PROCESS)
	@echo "==> Enlazando ejecutable de prueba $@"
	$(CC) $(LDFLAGS_EXEC) $^ -o $@
	@echo "==> Ejecutable de prueba $(TARGET_TEST_DEBUG) creado."

# --- Reglas de Compilación ---

# Regla genérica para compilar archivos C a objeto
$(OBJ_DIR)/%.o: $(SRC_C_DIR)/%.c | $(OBJ_DIR)
	@echo "==> Compilando C $< -> $@"
	$(CC) $(CFLAGS) -c $< -o $@

# Regla genérica para compilar archivos ASM a objeto
$(OBJ_DIR)/%.o: $(SRC_ASM_DIR)/%.asm | $(OBJ_DIR)
	@echo "==> Ensamblando $< -> $@"
	$(NASM) $(NASMFLAGS) $< -o $@

# Regla para crear el directorio de objetos si no existe
$(OBJ_DIR):
	@echo "==> Creando directorio de objetos $(OBJ_DIR)"
	mkdir -p $(OBJ_DIR)

# --- Reglas de Ejecución y Depuración ---

# Regla para ejecutar el cliente Python (asume que la lib ya está compilada)
run: $(TARGET_LIB)
	@echo "==> Ejecutando cliente Python..."
	python3 $(PYTHON_CLIENT)

# Regla para iniciar GDB con el programa de prueba
# Simplemente lanza GDB, tú escribes los comandos manualmente.
gdb: $(TARGET_TEST_DEBUG)
	@echo "==> Iniciando GDB con $(TARGET_TEST_DEBUG)..."
	@echo "    Usa comandos como: b main, b test_procesador.c:13, b procesar_gini_asm, r, si, ni, c, info reg, x/16xw \$esp"
	gdb $(TARGET_TEST_DEBUG)

# Regla para iniciar GDB y establecer breakpoints iniciales automáticamente
# Establece los puntos de interrupción clave y ejecuta 'run'.
# Te dejará detenido en el primer breakpoint (probablemente 'main').
debug: $(TARGET_TEST_DEBUG)
	@echo "==> Iniciando GDB con breakpoints y 'run' para $(TARGET_TEST_DEBUG)..."
	gdb -ex "b main" \
	    -ex "b test_procesador.c:13" \
	    -ex "b procesar_gini_asm" \
	    -ex "b test_procesador.c:15" \
	    -ex "run" \
	    $(TARGET_TEST_DEBUG)
# --- Regla de Limpieza (CON DEBUGGING ECHO) ---

clean:
	@echo "==> Limpiando archivos generados..."
	# Mostrar los valores de las variables antes de usarlas
	@echo "    Valor de OBJ_DIR: '$(OBJ_DIR)'"
	@echo "    Valor de TARGET_LIB: '$(TARGET_LIB)'"
	@echo "    Valor de TARGET_TEST_DEBUG: '$(TARGET_TEST_DEBUG)'"

	# Comando para borrar los .o
	@echo "    Intentando ejecutar: rm -f $(OBJ_DIR)/*.o"
	rm -f $(OBJ_DIR)/*.o

	# Comando para borrar la librería y el ejecutable
	@echo "    Intentando ejecutar: rm -f $(TARGET_LIB) $(TARGET_TEST_DEBUG)"
	rm -f $(TARGET_LIB) $(TARGET_TEST_DEBUG)

	# Opcionalmente, si quieres borrar el directorio obj descomenta la siguiente línea
	# rm -rf $(OBJ_DIR)
	@echo "==> Limpieza completa."

.PHONY: all clean run gdb debug