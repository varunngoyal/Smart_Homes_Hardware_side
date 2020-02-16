#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <ESP8266WiFiMulti.h>
#include "raspi_properties.h"

#define O_PIN LED_BUILTIN
#define LDR A0

int flag_ldr = 0;
int intensity = 0;
int flag_temp = 0;

ESP8266WiFiMulti wifiMulti;
boolean connectioWasAlive = true;


//const char* ssid = "TP-LINK_1784";
//const char* password = "asdfghjkl";
//const char* ssid = "Get your own";
//const char* password = "Tharki@777";

/*const char* mqtt_server = "tailor.cloudmqtt.com";

const char *mqtt_user = "ghleymma";
const char *mqtt_pass = "jmvoCCetDGiy";*/

/*const char* mqtt_server = "192.168.0.112";
const int   mqtt_port_no = 1883;
const char* mqtt_user = "pi";
const char* mqtt_pass = "mike";*/

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
  wifiMulti.addAP("ROHAN", "vaibhav018");
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

  randomSeed(micros());

  Serial.println("");
  
}

void publish_to_conf()
{
  //char topics[100][100] = {"301", "401"};
  
  //publishing messages on startup
  char message[200] = "{ \"type\" : \"ldr\", \"topic\" :\"";
  strcat(message, "301\"");
  strcat(message,",\"start\" : \"0\", \"end\" : \"0\", \"message\" : \"0\", \"Watt\": \"10\"," );
  strcat(message,"\"duty_cycle\":\"10\", \"category\": \"sensor\", \"ack_val\": \"null\"}");
  Serial.println(message);                    
  client.publish("conf", message);
  Serial.println("led information published on request to conf!");
  
  char message1[200] = "{ \"type\" : \"temp\", \"topic\" :\"";
  strcat(message1, "401\"");
  strcat(message1,",\"start\" : \"0\", \"end\" : \"0\", \"message\" : \"0\", \"Watt\": \"10\"," );
  strcat(message1,"\"duty_cycle\":\"10\", \"category\": \"sensor\", \"ack_val\": \"null\"}");
  Serial.println(message1);
  client.publish("conf", message1);
  Serial.println("fan information published on request to conf!");

}

void reconnect() {
  while(!client.connected()) {

      String clientId = "ESP8266Client-";
      clientId += String(random(0xffff), HEX);

      if(client.connect(clientId.c_str(), mqtt_user, mqtt_pass)) {
        Serial.print("connected to mqtt server ");
        Serial.println(mqtt_server);
        publish_to_conf();
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

  int i;
  Serial.print("[");
  for(i=0;i< length;i++) {

    //Serial.print((char)payload[i]);
    payloadstr[i] = (char)payload[i];
   Serial.print(payloadstr[i]);
  }
  Serial.println("]"); 

  payloadstr[i] = '\0';

    char topic1[100];
    strcpy(topic1, topic);

//    //if send is true from check status code, then send device info
//    if(strcmp(payloadstr, "check") == 0) {
//      char message[] = "{\"ack_message\": \"";
//      strcat(message, topic1);
//      strcat(message, "\"}");
//      client.publish("ack", message);
//      Serial.println("device information published on request to ack!");
//      Serial.print(topic1);
//    }

    if(strcmp("301", topic1) == 0) { //ldr
        intensity = analogRead(LDR);
        flag_ldr = 1;
    } else if(strcmp("401", topic1) == 0) { //temp
        flag_temp = 1;
    }
}



void setup() {
  // put your setup code here, to run once:
  pinMode(A0, INPUT);
  
  Serial.begin(9600);
  setup_wifi();

  //*********************server name and port*************
  PubSubClient temp = client.setServer(mqtt_server, 1883); 
  
  Serial.print("connected: ");
  Serial.println(temp.connected());
  Serial.print("state: ");
  Serial.println(temp.state());
  
  client.setCallback(callback);

  publish_to_conf();
  reconnect();
  
  //subscribing to various topics
//  char* topics[] = {"101", "201"};
//
//  //publish_to_conf();
//
//  for(int i=0;i<2;i++)
//  {
//     if(client.subscribe(topics[i], 0) == true)
//     {
//        Serial.print("subscribed successfully to : ");
//        Serial.println(topics[i]); 
//     } else {
//        Serial.print("subscription failed! : ");
//        Serial.println(topics[i]);  
//     } 
//
//  }

    
  //delay(100);
  //publish_to_conf();
  if(client.subscribe("301", 0))
  {
     Serial.print("subscribed successfully to : ");
     Serial.println("301"); 
  } else {
     
     Serial.print("subscription failed! : ");
  }
  if(client.subscribe("401", 0))
  {
     Serial.print("subscribed successfully to : ");
     Serial.println("401"); 
  } else {
     
     Serial.print("subscription failed! : ");
  }
}

void loop() {
  // put your main code here, to run repeatedly:

  if (wifiMulti.run() != WL_CONNECTED) {
    Serial.println("WiFi not connected!");
    delay(1000);
  }
  
  if(!client.connected()) {
    Serial.println("Not yet connected..");
    reconnect();
  }
  client.loop();

  if(flag_ldr)
  {
    char intensity_str[100];
    itoa(intensity, intensity_str, 10);
    char message[] = "{\"ack_message\": \"301\", \"ack_val\": \"";
    strcat(message, intensity_str);
    strcat(message, "\" }");
    
    client.publish("ack", message);
    delay(10);
    client.publish("ack", message);
    delay(10);
    client.publish("ack", message);
      
    flag_ldr = 0;
  }

  if(flag_temp)
  {
    char temp_str[100];
    itoa(random(0,51), temp_str, 10);
    char message1[] = "{\"ack_message\": \"401\", \"ack_val\": \"";
    strcat(message1, temp_str);
    strcat(message1, "\" }");
    client.publish("ack", message1); 
    delay(10);
    client.publish("ack", message1); 
    delay(10);
    client.publish("ack", message1); 
    
    flag_temp = 0;
  }

  /*digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);*/

}
