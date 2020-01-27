#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ESP8266WiFiMulti.h>

ESP8266WiFiMulti wifiMulti;
boolean connectioWasAlive = true;

const int analog_ip = A0;
int inputval = 0;
//const char* ssid = "TP-LINK_1784";
//const char* password = "asdfghjkl";
//const char* ssid = "Get your own";
//const char* password = "Tharki@777";

const char* mqtt_server = "192.168.0.102"; //######################## (server)

const char *mqtt_user = "pi";               //######################## (username)
const char *mqtt_pass = "mike";           //######################## (password)

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
int flag = 0;

void setup_wifi()
{
  delay(100);
  // We start by connecting to a WiFi network
  wifiMulti.addAP("TP-LINK_1784", "asdfghjkl");
  //wifiMulti.addAP("ROOTB", "asdfghjkl");
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
  /*Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }*/

  randomSeed(micros());

  Serial.println("");

}

void reconnect() {
  while (!client.connected()) {

    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str(), mqtt_user, mqtt_pass)) {
      Serial.println("connected");

      client.publish("outTopic", "hello world");

      client.subscribe("inTopic");
    } else {
      Serial.print("failed");
      delay(5000);
    }
  }

}

void callback(char* topic, byte* payload, unsigned int length) {
  //pinMode(LED_BUILTIN, OUTPUT);
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.println("] ");

  char payloadstr[100];


  int i;
  for (i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    payloadstr[i] = (char)payload[i];

  }
  payloadstr[i] = '\0';
  Serial.print("string form: ");
  Serial.println(payloadstr);

  if(strcmp(topic, "ldr") == 0) //message from ldr
  {
    if (strcmp(payloadstr, "ON") == 0)
    {
        flag = 1;     
    }
    else if (strcmp(payloadstr, "OFF") == 0)
    {
          Serial.println("ldr OFF!"); 
          flag = 0;    
    }
  }
  else {    //message from led2
      int payloadint = atoi(payloadstr);

      analogWrite(D8, 1024 - payloadint);

      Serial.println(1024 - payloadint);
  }
  /*
    Serial.println();
    //Serial.println(payloadstr1);


    //if else to on/off led

    if(strcmp(payloadstr, "ON") == 0)
    {
    //on the led
    Serial.println("on led success");
    digitalWrite(LED_BUILTIN, LOW);

    } else if(strcmp(payloadstr, "OFF") == 0){
    Serial.println("OFF led success");
    digitalWrite(LED_BUILTIN, HIGH);

    } else {
    Serial.print(strcmp((char*)payload, "OFF"));
    Serial.print("message is ");
    Serial.println((char*)payload);
    //Serial.println(payload);
    }*/

}



void setup() {
  // put your setup code here, to run once:
  pinMode(A0, INPUT);
  Serial.begin(9600);
  setup_wifi();


  client.setServer(mqtt_server, 1883); //server name and port*************
  client.setCallback(callback);
  reconnect();
  if (client.subscribe("ldr", 0) == true)
  {
    Serial.println("subscription to ldr topic successful!");
  }
  else {
    Serial.println("subscription to ldr topic failed!");
  }

  if(client.subscribe("led2", 0) == true)
  {
    Serial.println("subscription to led2 successful!");  
  }
  else {
    Serial.println("subscription to led2 failed!");  
  }
  


}

void loop() {
  // put your main code here, to run repeatedly:
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if(flag == 1)
  {
      int val;
      char valstr[100];
            
      val = analogRead(A0);
      itoa(val, valstr, 10);  //convert val to string
      client.publish("led1", valstr);
       
      Serial.print("Message: ");
      Serial.println(valstr); 
      delay(1000);
  }


  /*int val = analogRead(A0);

  char valstr[100];
  itoa(val, valstr, 10);
  Serial.print("Message: ");
  Serial.println(valstr);

  delay(1000);
  client.publish("abc", valstr);*/
}
