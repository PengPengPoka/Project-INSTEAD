HardwareSerial Serial2(PA10, PA9);

#define SENSOR1 PC0
#define SENSOR2 PC1
#define SENSOR3 PC4
#define SENSOR4 PC5
#define SENSOR5 PA4
#define SENSOR6 PA5
#define SENSOR7 PA6
#define SENSOR8 PA7

void setup() {
  Serial2.begin(115200);
  analogReadResolution(16);
  pinMode(SENSOR1, INPUT);
  pinMode(SENSOR2, INPUT);
  pinMode(SENSOR3, INPUT);
  pinMode(SENSOR4, INPUT);
  pinMode(SENSOR5, INPUT);
  pinMode(SENSOR6, INPUT);
  pinMode(SENSOR7, INPUT);
  pinMode(SENSOR8, INPUT);
}

void loop() {
  if (Serial2.available()) {
    String received_data = Serial2.readStringUntil('\n');

    int received_values[2];
    int value_index = 0;
    char separator = '#';
    int start = 0;

    received_data.trim();  // Hapus \n di akhir
    // Serial2.println(received_data);

    for (int i = 0; i < received_data.length(); i++) {
      if (received_data[i] == separator || received_data[i] == '\n') {
        received_values[value_index] = received_data.substring(start, i).toInt();  // Mengonversi string menjadi integer
        value_index++;
        start = i + 1;
      }
    }

    if (value_index > 0) {
      received_values[value_index] = received_data.substring(start).toInt();
    }

    // if (value_index >= 2) {
    int delay_ms = received_values[0];
    // Serial2.println(delay_ms);
    int amount = received_values[1];
    // Serial2.println(amount);
    // }

    for (int i = 0; i < amount; i++) {
      Serial2.print(analogRead(SENSOR1));
      Serial2.print("#");
      Serial2.print(analogRead(SENSOR2));
      Serial2.print("#");
      Serial2.print(analogRead(SENSOR3));
      Serial2.print("#");
      Serial2.print(analogRead(SENSOR4));
      Serial2.print("#");
      Serial2.print(analogRead(SENSOR5));
      Serial2.print("#");
      Serial2.print(analogRead(SENSOR6));
      Serial2.print("#");
      Serial2.print(analogRead(SENSOR7));
      Serial2.print("#");
      Serial2.print(analogRead(SENSOR8));
      Serial2.print("\n");
      delay(delay_ms);
    }
  }
}
