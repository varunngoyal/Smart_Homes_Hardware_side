#include <ArduinoJson.h>

//#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ESP8266WiFiMulti.h>

#define O_PIN LED_BUILTIN
//#define con_topic conf

ESP8266WiFiMulti wifiMulti;
boolean connectioWasAlive = true;

StaticJsonDocument<300> doc;

char id[] =
      "{\"company\":\"samsung\",\"type\":\"led\",\"topic\":\"led1\",\"uid\":1001}";
  
//const char* ssid = "TP-LINK_1784";
//const char* password = "asdfghjkl";
//const char* ssid = "Get your own";
//const char* password = "Tharki@777";

/*const char* mqtt_server = "tailor.cloudmqtt.com";

const char *mqtt_user = "ghleymma";
const char *mqtt_pass = "jmvoCCetDGiy";*/

const char* mqtt_server = "192.168.1.104";
const char* mqtt_topic = "led1";
const char* mqtt_user = "pi";
const char* mqtt_pass = "mike";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup_wifi()
{
  //WiFi.mode(WIFI_STA);
  
  //wifiMulti.addAP("TP-LINK_1784", "asdfghjkl");
  //wifiMulti.addAP("ROOTB", "asdfghjkl");
  wifiMulti.addAP("Get Your Own", "Tharki@777");
   // wifiMulti.addAP("RUMS", "nellai4161");        //anirudh hall wifi
  //wifiMulti.addAP("JioFi3_5BE5AC", "asdfghjkl"); // anirudh jio wifi
  
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
        client.publish("conf", id);
        Serial.println("publishing jason initialization");//once get connected to server pass self identity
        
      } else {
        Serial.print("failed");
        delay(2000);
      }
  }
  
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


    int payloadint = atoi(payloadstr);

    analogWrite(O_PIN, 1024 - payloadint);

    Serial.println(1024 - payloadint);

  
  

}



void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(O_PIN, LOW);
  delay(100);
  digitalWrite(O_PIN, HIGH);
  delay(100);
  Serial.begin(9600);
  setup_wifi();

 
  PubSubClient temp = client.setServer(mqtt_server, 1883); //server name and port*************
  Serial.print("connected: ");
  Serial.println(temp.connected());
  Serial.print("state: ");
  Serial.println(temp.state());
  
  client.setCallback(callback);
  reconnect();
  if(client.subscribe("led1", 0) == true)
  {
    Serial.println("subscription to led1 successful!");  
  }
  else {
    Serial.println("subscription to led1 failed!");  
  }
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

  //delay(5000);
  //client.publish("conf","delayed pass");
 
  //client.publish("dht", cstr);
  //client.publish("bmp", cshr);

  //h++;
  //t++;
}
