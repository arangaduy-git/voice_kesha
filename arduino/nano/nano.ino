#include <Servo.h>
#include "DHT.h"

DHT dht(9, DHT11);
Servo window;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(A0, INPUT); // окно ESP
  pinMode(A1, INPUT); // ванна ESP
  pinMode(A2, INPUT); // свет ESP

  pinMode(A6, INPUT); // дождь

  dht.begin();
  window.attach(3); // окно NANO
  pinMode(5, OUTPUT); // ванна NANO
  pinMode(6, OUTPUT); // свет NANO
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("Rain: ");
  Serial.print(analogRead(A6));
  Serial.print("     |      Температура: ");
  Serial.println(dht.readTemperature());
  if (digitalRead(A0) == 1) {
    window.write(135);
  }
  if (digitalRead(A0) == 0) {
    window.write(45);
  }

  digitalWrite(5, digitalRead(A1));
  digitalWrite(6, digitalRead(A2));
}
