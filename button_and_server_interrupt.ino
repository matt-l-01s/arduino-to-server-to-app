#include <WiFi.h>
#include <WiFiClient.h>
#include <SPI.h>

#define PACKET_SIZE 6
#define ENTER_BUTTON_PIN 34
#define EXIT_BUTTON_PIN 35

byte serverIP[] = { 180, 235, 234, 95 };
int serverPort = 9005;
char ssid[] = "your network SSID here";          //  your network SSID (name)l-down resisto
char pass[] = "your network password here";   // your network password

//send it when ESP32 first connect to the server.
char Header[] = { 0x1, 0x3, 'S', 'I', 'T',};

//The first three bytes are the number of button pushed at the entrance.
//The last three bytes are the number of button pushed at the exit.

byte packet[PACKET_SIZE] = {0X0, 0X0, 0X0, 0x0, 0x0, 0x0};

const unsigned long cool_time = 5000;
volatile bool sending_flag = false;
volatile unsigned long enter_num = 0;
volatile unsigned time_pushed_EnterButton = 0;
volatile unsigned long exit_num = 0;
volatile unsigned time_pushed_ExitButton = 0;


//It is called when button is just released at the entrance.
void IRAM_ATTR offEnterButton(){
  unsigned long now_time = millis();
  if(now_time - time_pushed_EnterButton > cool_time){
    ++enter_num;
    sending_flag = true;
    
    Serial.print("enter");
    Serial.println(enter_num);
  
  }
  time_pushed_EnterButton = now_time;
}

//It is called when button is just released at the exit.
void IRAM_ATTR offExitButton(){
  unsigned long now_time = millis();
  if(now_time - time_pushed_ExitButton > cool_time){
    ++exit_num;
    sending_flag = true;
    
    Serial.print("exit");
    Serial.println(exit_num);
  
  }
  time_pushed_ExitButton = now_time;
}

WiFiClient client;

void sendData(){
  START:
  
  sending_flag = false;
  
  //make packet
  packet[0] = (byte)((enter_num >> 16) /*% 0x100*/);
  packet[1] = (byte)((enter_num >> 8) % 0x100);
  packet[2] = (byte)((enter_num >> 0) % 0x100);
  packet[3] = (byte)((exit_num >> 16) % 0x100);
  packet[4] = (byte)((exit_num >> 8) % 0x100);
  packet[5] = (byte)((exit_num >> 0) % 0x100);
  
  //If there is an interrupt while making the packet, try remaking.
  if(sending_flag) goto START;
  
  client.write(packet, PACKET_SIZE);
}



void setup() {
  Serial.begin(9600);

  //connecting to WiFi
  Serial.print("SSID: ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  int TTL = 20;
  Serial.print("Connecting to WiFi");
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

  //connecting to server
  client.connect(serverIP, serverPort);
  TTL = 20;
  Serial.print("Connecting to Server");
  delay(5000);
  while( !client.connected() && --TTL>=0) {
    client.connect(serverIP, serverPort);
    delay(5000);
    Serial.print(".");
  if( !client.connected()) {
    Serial.println("Couldn't get a Server connection");
    return;
  }
  Serial.println("\nConnected to Server");
  // Make a channel
  client.write(Header);

  //seting Pins and attaching Interrupt Functions
  pinMode(ENTER_BUTTON_PIN, INPUT);
  attachInterrupt(ENTER_BUTTON_PIN, offEnterButton, FALLING);
  pinMode(EXIT_BUTTON_PIN, INPUT);
  attachInterrupt(EXIT_BUTTON_PIN, offExitButton, FALLING);
}

#define INTERVAL 10000
void loop() {
  //send data to server at 10000 milliseconds intervals
  delay(INTERVAL);
  if(sending_flag) sendData();
}
