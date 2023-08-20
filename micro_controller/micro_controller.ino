HardwareSerial Serial2(PA10, PA9);

#define POT1 PC0
#define POT2 PC1
#define POT3 PC4
#define POT4 PC5

void setup() {
  Serial2.begin(115200);
  // pinMode(PA2, OUTPUT);
  pinMode(POT1, INPUT);
  pinMode(POT2, INPUT);
  pinMode(POT3, INPUT);
  pinMode(POT4, INPUT);
}

void loop() {
  // digitalWrite(PA2, HIGH);
  
  // Serial2.println("POT 1: ");
  // delay(500);
  // digitalWrite(PA2, LOW);
  Serial2.print(analogRead(POT1));
  Serial2.print("#");
  // Serial2.println("POT 2: ");
  Serial2.print(analogRead(POT2));
  Serial2.print("#");
  Serial2.print(analogRead(POT3));
  Serial2.print("#");
  Serial2.print(analogRead(POT4));
  // Serial2.print("#");
  Serial2.print("\n");
  
  delay(100);
}
