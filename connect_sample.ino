#include <WiFi.h>
#include <WiFiClient.h>
#include <SPI.h>


byte serverIP[] = { 180, 235, 234, 95 };
int serverPort = 9005;
char ssid[] = "your network SSID here";       // To do
char pass[] = "your network password here";   // To do
char Header[] = { 0x1, 0x3, 'S', 'I', 'T',};



WiFiClient client;

void setup() {
  Serial.begin(9600);

  WiFi.begin(ssid, pass);
  int TTL = 20;
  Serial.println("Connecting to WiFi");
  Serial.print("SSID: ");
  Serial.println(ssid);
  while( WiFi.status() != WL_CONNECTED && --TTL>=0) {
    delay(500);
    Serial.print(".");
  }
  if( WiFi.status() != WL_CONNECTED) {
    Serial.println("\nCouldn't get a wifi connection");
    return;
  }
  Serial.println("\nConnected to wifi with IP Address: ");
  Serial.println(WiFi.localIP());


  client.connect(serverIP, serverPort);
  TTL = 20;
  Serial.print("Connecting to Server");
  delay(5000);
  while( !client.connected() && --TTL>=0) {
    client.connect(serverIP, serverPort);
    delay(50000);
    Serial.print(".");
  }
  if( !client.connected()) {
    Serial.println("Couldn't get a Server connection");
    return;
  }
  Serial.println("\nConnected to Server");
  client.write(Header);
}

byte up = 1;
byte down = -1;
  
void loop() {

  client.write(up);
  Serial.println("write  1");
  delay(5000);

  client.write(down);
  Serial.println("write -1");
  delay(5000);
}
