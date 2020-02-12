

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}


void loop() {
  // Leitura analogica da porta A0
  int sensorValue = analogRead(A0);
  // Converte a leitura analógica (10 bits; de 0 - 1023) para um nível de tensão (0 - 5V):
  
  float voltage = sensorValue * (5.0 / 1023.0);
  
  Serial.println(voltage);
  float freq = 400;
  delay(1000.0/freq);
}
