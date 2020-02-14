#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <ESP8266WiFiMulti.h>

#define O_PIN LED_BUILTIN
#define FAN D5

ESP8266WiFiMulti wifiMulti;
boolean connectioWasAlive = true;


//const char* ssid = "TP-LINK_1784";
//const char* password = "asdfghjkl";
//const char* ssid = "Get your own";
//const char* password = "Tharki@777";

/*const char* mqtt_server = "tailor.cloudmqtt.com";

const char *mqtt_user = "ghleymma";
const char *mqtt_pass = "jmvoCCetDGiy";*/

const char* mqtt_server = "192.168.1.104";
const int   mqtt_port_no = 1883;
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

  randomSeed(micros());

  Serial.println("");
  
}

void publish_to_conf()
{
  //char topics[100][100] = {"101", "201"};
  
  //publishing messages on startup
  char message[200] = "{ \"type\" : \"led\", \"topic\" :";
  strcat(message, "101");
  strcat(message,",\"start\" : \"0\", \"end\" : \"0\", \"message\" : \"0\", \"Watt\": \"10\",\"duty_cycle\":\"10\"}" );
  Serial.println(message);                    
  client.publish("conf", message);
  Serial.println("led information published on request to conf!");

  char message1[200] = "{ \"type\" : \"fan\", \"topic\" :";
  strcat(message1, "201");
  strcat(message1,",\"start\" : \"0\", \"end\" : \"0\", \"message\" : \"0\", \"Watt\": \"10\",\"duty_cycle\":\"10\"}" );
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

  StaticJsonDocument<300> doc;

    char topic1[100];
    strcpy(topic1, topic);
    //if send is true from check status code, then send device info
    char message[] = "{\"ack_message\": \"";
    strcat(message, topic1);
    strcat(message, "\"}");
    client.publish("ack", message);
    Serial.println("device information published on request to ack!");
  Serial.print(topic1);

    if (isDigit(payloadstr[0]))
    {
      Serial.println("only numbers allowed!");
      int payloadint = atoi(payloadstr);

      if(strcmp(topic1, "101") == 0) {
        Serial.println();
        analogWrite(O_PIN, 1024 - payloadint);
        
        
      } else if (strcmp(topic1, "201") == 0) {
        if(payloadint <=5 && payloadint >= 0)
          analogWrite(FAN,payloadint*200);
      }
    }

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

  //*********************server name and port*************
  PubSubClient temp = client.setServer("192.168.1.104", 1883); 
  
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
  if(client.subscribe("101", 0))
  {
     Serial.print("subscribed successfully to : ");
     Serial.println("101"); 
  } else {
     
     Serial.print("subscription failed! : ");
  }
  if(client.subscribe("201", 0))
  {
     Serial.print("subscribed successfully to : ");
     Serial.println("201"); 
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

  /*digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);*/

}
