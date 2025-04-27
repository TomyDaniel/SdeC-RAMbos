# Makefile for Protected Mode Bootloader (Boot Sector Version)

ASM = nasm
ASMFLAGS = -f bin

TARGET = bootloader.img
SRC = modoprotegido.asm

QEMU = qemu-system-i386
# -fda $(TARGET): Usa la imagen como disquete A
# -boot a: Intenta arrancar desde el disquete primero
QEMUFLAGS = -fda $(TARGET) -boot a -no-reboot -d int

all: $(TARGET)