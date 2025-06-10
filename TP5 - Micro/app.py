import os
import time
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DEVICE_PATH = "/dev/signal_generator"

class UserApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Visualizador de Señales - TP Real")
        self.geometry("800x600")

        # Intentar abrir el dispositivo del driver
        try:
            self.device_fd = os.open(DEVICE_PATH, os.O_RDWR)
        except OSError as e:
            # Si falla, mostramos un error en la GUI y cerramos
            error_label = ttk.Label(self, text=f"Error: No se pudo abrir {DEVICE_PATH}\n{e}\n\nAsegúrate de haber cargado el módulo del kernel con:\nsudo insmod signal_driver.ko\ny de tener los permisos correctos:\nsudo chmod 666 {DEVICE_PATH}", padding=20)
            error_label.pack(expand=True)
            print(f"Error al abrir el dispositivo: {e}")
            self.after(5000, self.destroy) # Cerrar la app después de 5 seg
            return

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Datos para el gráfico
        self.time_data = []
        self.signal_data = []
        self.current_signal_type = "Cuadrada"

        self._setup_ui()
        
        # Iniciar la primera lectura y el bucle de actualización
        self.update_plot()

    def _setup_ui(self):
        control_frame = ttk.Frame(self, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(control_frame, text="Seleccionar Señal:").pack(side=tk.LEFT, padx=5)
        
        btn_s1 = ttk.Button(control_frame, text="Señal 1 (Cuadrada)", command=lambda: self.change_signal(1))
        btn_s1.pack(side=tk.LEFT, padx=5)

        btn_s2 = ttk.Button(control_frame, text="Señal 2 (Triangular)", command=lambda: self.change_signal(2))
        btn_s2.pack(side=tk.LEFT, padx=5)

        fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def change_signal(self, signal_id):
        """Envía el comando al driver para cambiar de señal."""
        try:
            if signal_id == 1:
                os.write(self.device_fd, b'1')
                self.current_signal_type = "Cuadrada"
            elif signal_id == 2:
                os.write(self.device_fd, b'2')
                self.current_signal_type = "Triangular"
            
            # Resetear el gráfico, como pide el TP
            print(f"App: Gráfico reseteado para la señal {self.current_signal_type}")
            self.time_data = []
            self.signal_data = []
            self.plot_data() # Actualizar inmediatamente para ver el cambio de título
        except OSError as e:
            print(f"Error al escribir en el dispositivo: {e}")

    def update_plot(self):
        """Pide datos al driver y actualiza el gráfico."""
        try:
            # Leemos del driver. El driver nos da una cadena "tiempo,valor\n"
            raw_data = os.read(self.device_fd, 32).decode('utf-8').strip()
            if raw_data:
                # Parseamos la cadena
                t_str, val_str = raw_data.split(',')
                t, value = int(t_str), int(val_str)

                # Añadimos solo si es un dato nuevo
                if not self.time_data or t > self.time_data[-1]:
                    self.time_data.append(t)
                    self.signal_data.append(value)
                    
                    if len(self.time_data) > 30:
                        self.time_data.pop(0)
                        self.signal_data.pop(0)
                    
                    self.plot_data()
        except (OSError, ValueError) as e:
            print(f"Error leyendo o parseando datos del driver: {e}")

        # Programamos la próxima actualización en 1000 ms (1 segundo)
        self.after(1000, self.update_plot)
        
    def plot_data(self):
        """Dibuja los datos actuales en el gráfico."""
        self.ax.clear()
        
        self.ax.plot(self.time_data, self.signal_data, marker='o', linestyle='-')
        
        self.ax.set_title(f"Señal: {self.current_signal_type}")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Valor (unidades)")
        self.ax.grid(True)
        
        if self.signal_data:
            min_val, max_val = min(self.signal_data), max(self.signal_data)
            self.ax.set_ylim(min_val - 0.5, max_val + 0.5)

        self.canvas.draw()
        
    def on_closing(self):
        """Limpia los recursos antes de cerrar."""
        if hasattr(self, 'device_fd'):
            print("Cerrando el descriptor del dispositivo...")
            os.close(self.device_fd)
        self.destroy()

if __name__ == "__main__":
    app = UserApplication()
    app.mainloop()