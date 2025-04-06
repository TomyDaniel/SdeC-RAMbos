#include <Arduino.h>


const int loop_count = 1000000;


void suma_enteros() {
  volatile int acc = 0;
  for (int i = 0; i < 100; i++) {
    acc += 1;
  }
}


void setup() {
  Serial.begin(115200);
  delay(1000);


  int freqs[] = {80, 160, 240};


  for (int i = 0; i < 3; i++) {
    setCpuFrequencyMhz(freqs[i]);
    delay(100);
   
    Serial.printf("Probando con frecuencia: %d MHz\n", getCpuFrequencyMhz());


    unsigned long start = micros(); // Mayor precisión
    for (int j = 0; j < loop_count; j++) {
      suma_enteros();
    }
    unsigned long end = micros();


    float total_seconds = (end - start) / 1000000.0;
    Serial.printf("Tiempo total de ejecución: %.6f segundos\n", total_seconds);
  }
}


void loop() {}
