#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <ESP8266WiFiMulti.h>

#define O_PIN LED_BUILTIN

ESP8266WiFiMulti wifiMulti;
boolean connectioWasAlive = true;


//const char* ssid = "TP-LINK_1784";
//const char* password = "asdfghjkl";
//const char* ssid = "Get your own";
//const char* password = "Tharki@777";

/*const char* mqtt_server = "tailor.cloudmqtt.com";

const char *mqtt_user = "ghleymma";
const char *mqtt_pass = "jmvoCCetDGiy";*/

const char* mqtt_server = "192.168.1.103";
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
  
  wifiMulti.addAP("TP-LINK_1784", "asdfghjkl");
  //wifiMulti.addAP("ROOTB", "asdfghjkl");
  wifiMulti.addAP("Get Your Own", "Tharki@777");
  wifiMulti.addAP("RUMS", "nellai4161");        //anirudh hall wifi
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
        Serial.print("connected to mqtt server ");
        Serial.println(mqtt_server);
      } else {
        Serial.print("reconnect to mqtt server failed: ");
        Serial.println(mqtt_server);

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
  Serial.print("[");
  for(i=0;i< length;i++) {

    //Serial.print((char)payload[i]);
    payloadstr[i] = (char)payload[i];
   Serial.print(payloadstr[i]);
  }
  Serial.println("]"); 

  payloadstr[i] = '\0';

  //convert char array to json
  StaticJsonDocument<300> doc;

  deserializeJson(doc, payloadstr);
  /*
  char sendvalue[100];
  strcpy(sendvalue, doc["send"]);
  Serial.println(sendvalue);
  */
  //if send is true from check status code, then send device info
  if(strcmp(doc["send"],"true") == 0) {
    delay(100);
    client.publish("conf", "{\"company\":\"samsung\", \"type\":\"led\",\"modelno\":\"123456\", \"uid\":\"ABC123\", \"topic\":\"led1\"}");
    Serial.println("device information published on request to conf!");
  }
  

    /*
    int payloadint = atoi(payloadstr);

    analogWrite(O_PIN, 1024 - payloadint);

    Serial.println(1024 - payloadint);
    */
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
    
  }/* else if(strcmp(payloadstr, "LDR") == 0){
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


  //publishing status of device to topic at startup
  //********************************************************************8
  StaticJsonDocument<300> doc;
 
  doc["type"] = "led";
  doc["category"] = "LED_NORMAL";
  doc["power_cons"] = 50;
  doc["company_name"] = "PHILLIPS";
  doc["serial_no"] = "0x28423875932532";
  doc["uptime"] = "40hrs";
  JsonArray values = doc.createNestedArray("values");

  Serial.println("hello");
  values.add(20);
  values.add(21);
  values.add(23);
  
  char JSONmessageBuffer[200];
  //doc.printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
  serializeJson(doc, JSONmessageBuffer);
  Serial.println("Sending message to MQTT topic..");
  Serial.println(JSONmessageBuffer);

    if (client.publish("led1status", JSONmessageBuffer) == true) {
    Serial.println("Success sending message");
  } else {
    Serial.println("Error sending message");
  }

    //********************************************************************8
    client.publish("conf", "{\"company\":\"samsung\", \"type\":\"led\",\"modelno\":\"123456\", \"uid\":\"ABC123\", \"topic\":\"led1\"}");
    Serial.println("device information published on request to conf!");
  Serial.println("Hello close!");
  //subscribing to various topics
  if(client.subscribe("led1", 0) == true)
  {
    Serial.println("subscription to led1 successful!"); 
    Serial.println("Hello inside!"); 
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
