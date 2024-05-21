#include <ESP8266WiFi.h>

const char *ssid = "Kesha";
const char *password = "12345678";
const char *host = "192.168.34.164";
const String ID = "D-280823-111111";
const int port = 4578;                     

void setup() {
  // put your setup code here, to run once:

  pinMode(D5, OUTPUT); // окно
  pinMode(D6, OUTPUT); // ванна
  pinMode(D7, OUTPUT); // свет

  Serial.begin(9600);
  WiFi.mode(WIFI_OFF);
  delay(1000);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.print("Connecting");
  // Ждем соединения
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }                                          //Пока пытаемся соединиться отправляем в UART точки
  Serial.println("");                                          //Если удачно подключились
  Serial.print("Connected to ");                               //Пишем в UART:
  Serial.println(ssid);                                        //Название точки доступа
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());   
}

void loop() {
  // put your main code here, to run repeatedly:

  digitalWrite(D5, 0);
  digitalWrite(D6, 0);
  digitalWrite(D7, 0);

  delay(1000);
  Serial.print("connecting to ");
  Serial.println(host);

  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    return;
  }
  client.print(ID);
  Serial.println("connected");

  while (client.connected())
  {
    if (client.available()){
      String cmd = client.readStringUntil('\n');
      if (cmd != ""){
        Serial.println(cmd);
      }

      if (cmd == "W-1") {
        digitalWrite(D5, 1);
      }
      if (cmd == "W-0") {
        digitalWrite(D5, 0);
      }

      if (cmd == "B-1") {
        digitalWrite(D6, 1);
      }
      if (cmd == "B-0") {
        digitalWrite(D6, 0);
      }

      if (cmd == "L-1") {
        digitalWrite(D7, 1);
      }
      if (cmd == "L-0") {
        digitalWrite(D7, 0);
      }
    }
  }

  Serial.println();
  Serial.println("closing connection");
}
