; Mode: Real Mode 16 bits
bits 16
org 0x7C00

start:
    cli                 ; Disable interrupts

    ; Load GDT
    lgdt [gdt_ptr]

    ; Enable Protected Mode (set PE bit in CR0)
    mov eax, cr0
    or eax, 1
    mov cr0, eax

    ; Far jump to protected mode code segment
    jmp CODE_SEG:protected_mode

; Switch to 32-bit mode
bits 32
protected_mode:
    ; Load segment registers with DATA segment selector
    mov ax, DATA_SEG
    mov ds, ax
    mov ss, ax
    mov es, ax
    mov fs, ax
    mov gs, ax

    ; Setup stack
    mov esp, stack_top

    ; --- Test writing to read-only data segment ---
    mov edi, 0x00100000      ; Point inside data segment (base 0x00100000)
    mov eax, 0x12345678
    mov [edi], eax           ; Attempt to write (should cause a fault)

    ; If no fault occurs (unexpected), write to video memory
    mov edi, 0xb8000
    mov ah, 0x0F
    mov al, 'P'
    mov [edi], ax
    add edi, 2
    mov al, 'M'
    mov [edi], ax

halt_loop:
    hlt
    jmp halt_loop

; --- GDT and Related Structures ---

; GDTR pointer
gdt_ptr:
    dw gdt_end - gdt_start - 1   ; Size of GDT - 1
    dd gdt_start                 ; Linear address of GDT

; Global Descriptor Table

; Null descriptor
align 8
gdt_start:
gdt_null:
    dq 0x0000000000000000

; Code segment descriptor (base 0x00000000)
gdt_code:
    dw 0xFFFF        ; Limit low
    dw 0x0000        ; Base low
    db 0x00          ; Base middle
    db 0x9A          ; Access: execute/read, non-conforming, accessed=0
    db 0xCF          ; Flags: 4K granularity, 32-bit, Limit high
    db 0x00          ; Base high

; Data segment descriptor (base 0x00100000), read-only
; Access byte modified: 0x90 -> Read-only

align 8
gdt_data:
    dw 0xFFFF        ; Limit low
    dw 0x0000        ; Base low
    db 0x10          ; Base middle (0x0010_0000 >> 16 = 0x10)
    db 0x90          ; Access: data segment, read-only, accessed=0
    db 0xCF          ; Flags: 4K granularity, 32-bit, Limit high
    db 0x00          ; Base high

gdt_end:

; Selectors
CODE_SEG equ gdt_code - gdt_start
DATA_SEG equ gdt_data - gdt_start

; Stack definition
stack_top equ 0x90000    ; Stack located safely at 576 KB

; Fill up to 510 bytes and add boot signature
times 510-($-$$) db 0
dw 0xAA55
