#include <uMQTTBroker.h>
#include <MQTT.h>

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ESP8266WiFiMulti.h>


//######################################
#define redPin D8
#define greenPin D3
#define bluePin D1

//######################################

ESP8266WiFiMulti wifiMulti;
boolean connectioWasAlive = true;


//const char* ssid = "TP-LINK_1784";
//const char* password = "asdfghjkl";
//const char* ssid = "Get your own";
//const char* password = "Tharki@777";

const char* mqtt_server = "192.168.0.102";

const char *mqtt_user = "pi";
const char *mqtt_pass = "mike";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup_wifi()
{
  //WiFi.mode(WIFI_STA);
  
  wifiMulti.addAP("TP-LINK_1784", "asdfghjkl");
  wifiMulti.addAP("ROOTB", "asdfghjkl");
  wifiMulti.addAP("Get your own", "Tharki@777");
    wifiMulti.addAP("RUMS", "nellai4161"); //anirudh hall wifi
  wifiMulti.addAP("JioFi3_5BE5AC", "asdfghjkl"); // anirudh jio wifi
  int i = 0;
  while(wifiMulti.run() != WL_CONNECTED) {
    delay(1000);
    Serial.print(++i); Serial.print(' ');
  }
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());  
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  
  /*Normal WiFi Access Point
   * 
   * delay(100);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }*/

  randomSeed(micros());

  Serial.println("");
  
}

void reconnect() {
  while(!client.connected()) {

      String clientId = "ESP8266Client-";
      clientId += String(random(0xffff), HEX);

      if(client.connect(clientId.c_str(), mqtt_user, mqtt_pass)) {
        Serial.println("connected");
      } else {
        Serial.print("failed");
        delay(5000);
      }
  }
  
}

void setColor(int red, int green, int blue)
{
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);
}

void callback(char* topic, byte* payload, unsigned int length) {
  //pinMode(LED_BUILTIN, OUTPUT);
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");

  char payloadstr[100];

  //payloadstr1[0] = 'a';
  //payloadstr1[1] = '\0';
  //Serial.println(payloadstr1);

  int i;
  for(i=0;i< length;i++) {
    //Serial.print((char)payload[i]);
    payloadstr[i] = (char)payload[i];
    
  }
  payloadstr[i] = '\0';

  if(strcmp(topic, "colourled") == 0)
  {
    //change color of led 
    //###########################################################################
  
    int redInt, greenInt, blueInt;

    //e.g 15,5,200
    int i=0;
    char redstr[4], greenstr[4], bluestr[4];
    int k=-1;
    while(payloadstr[i] != ',')
    {
      redstr[++k] = payloadstr[i];
      i++;
    }
    ++i;
    redstr[++k] = '\0';
    redInt = atoi(redstr);
    
    k=-1;
    while(payloadstr[i] != ',')
    {
      greenstr[++k] = payloadstr[i];
      i++;    
    }
    ++i;
    greenstr[++k] = '\0';
    greenInt = atoi(greenstr);
    
    k=-1;
    while(payloadstr[i] != '\0')
    {
      bluestr[++k] = payloadstr[i];  
      i++;
    }
    bluestr[++k] = '\0';
    blueInt = atoi(bluestr);
    
    redInt = constrain(redInt, 0, 255);
    greenInt = constrain(greenInt, 0, 255);
    blueInt = constrain(blueInt, 0, 255);

    setColor(redInt, greenInt, blueInt);

    Serial.print("Red: ");
    Serial.print(redInt);
    Serial.print(" Green: ");
    Serial.print(greenInt);
    Serial.print(" Blue: ");
    Serial.print(blueInt);
    Serial.println();

    //#########################################################################

    
  }
  else if(strcmp(topic, "led1") == 0) 
  {
    int payloadint = atoi(payloadstr);

    analogWrite(D8, 1024 - payloadint);

    Serial.println(1024 - payloadint);
  }
  //Serial.println();
  //Serial.println(payloadstr1);

  
  //if else to on/off led
  
  /*if(strcmp(payloadstr, "ON") == 0)
  {
    //on the led
    Serial.println("on led success");    
    digitalWrite(LED_BUILTIN, LOW);
    
  } else if(strcmp(payloadstr, "OFF") == 0){
    Serial.println("OFF led success");    
    digitalWrite(LED_BUILTIN, HIGH);
    
  } else if(strcmp(payloadstr, "LDR") == 0){
    Serial.print(strcmp((char*)payload, "OFF"));    
    Serial.print("message is ");
    Serial.println((char*)payload);
    //Serial.println(payload);
      analogWrite(D8, 1024 - payloadint);

  Serial.println(1024 - payloadint);
  }*/
  //set intensity of lamp based on integer value recieved
 

  

}



void setup() {
  // put your setup code here, to run once:
  pinMode(D8, OUTPUT);
  //#####################################################################
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  //#####################################################################
  
  digitalWrite(D8, LOW);
  delay(100);
  digitalWrite(D8, HIGH);
  delay(100);
  Serial.begin(9600);
  setup_wifi();

  //####################################################################
  setColor(255, 0, 0);
  delay(500);
  setColor(0, 255, 0);
  delay(500);
  setColor(0, 0, 255);
  delay(500);
  setColor(255, 255, 255);
  //####################################################################
  
  client.setServer(mqtt_server, 13968); //server name and port*************
  client.setCallback(callback);
  reconnect();
  if(client.subscribe("led1", 0) == true)
  {
    Serial.println("subscription to led1 successful!");  
  }
  else {
    Serial.println("subscription to led1 failed!");  
  }
  //#################################################################

  if(client.subscribe("colourled", 0) == true)
  {
    Serial.println("Subscription to colourled successful!");  
  }
  else {
    Serial.println("subscription to colourled failed!");  
  }

  //#################################################################
}

void loop() {
  // put your main code here, to run repeatedly:

  if (wifiMulti.run() != WL_CONNECTED) {
    Serial.println("WiFi not connected!");
    delay(1000);
  }
  
  if(!client.connected()) {
    reconnect();
  }
  client.loop();
 
    //digitalWrite(LED_BUILTIN, LOW);
    //delay(5000);
    //digitalWrite(LED_BUILTIN, HIGH);


  /*static int h = 30; //random*************************
  static int t = 20; //random************************

  String hh = String(h);
  String msg = String(t);

  Serial.print("Publish message: ");
  Serial.println(msg);

  int numt = t;
  char cstr[16];
  itoa(numt, cstr, 10);

  int numh = h;
  char cshr[16];
  itoa(numh, cshr, 10);*/

 
  //client.publish("dht", cstr);
  //client.publish("bmp", cshr);

  //h++;
  //t++;
}
