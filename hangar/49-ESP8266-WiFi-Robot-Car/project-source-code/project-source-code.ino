/* include library */
#include <WiFi.h>


/* define port */
WiFiClient client;
WiFiServer server(80);

/* WIFI settings */
const char* ssid = "INVTech 2.4G";
const char* password = "INVTECH#2019";

/* data received from application */
String  data = "";


/* define L298N or L293D enable pins */
int motors1 = 2; /* GPIO14(D5) -> Motor-A Enable */
int motors2 = 4;
int lights_pin = 5; /* GPIO D5 -> Lights */
void setup()
{
  Serial.begin(115200);

  /* initialize motor enable pins as output */
  pinMode(motors1, OUTPUT);
  pinMode(motors2, OUTPUT);
  pinMode(lights_pin, OUTPUT);
  digitalWrite(lights_pin, HIGH);
  /* start server communication */
  connectWiFi();
  server.begin();
}

void loop()
{
    /* If the server available, run the "checkClient" function */
    client = server.available();
    if (!client) return;
    data = checkClient();
    Serial.println(data);
/************************ Run function according to incoming data from application *************************/

    /* If the incoming data is "forward", run the "MotorForward" function */
    if (data == "open") OpenHangar();
    /* If the incoming data is "backward", run the "MotorBackward" function */
    else if (data == "close") CloseHangar();
    /* If the incoming data is "left", run the "TurnLeft" function */
    else if (data == "stop") StopHangar();
    else if (data == "lights_on") LightsOn();
    /* If the incoming data is "right", run the "TurnRight" function */
    else if (data == "lights_off") LightsOff();
}

/********************************************* OPEN HANGAR *****************************************************/
void OpenHangar(void)
{
  digitalWrite(motors1, HIGH);
  digitalWrite(motors2, LOW);
}
/********************************************* CLOSE HANGAR *****************************************************/
void CloseHangar(void)
{
  digitalWrite(motors1, LOW);
  digitalWrite(motors2, HIGH);
}
/********************************************* STOP HANGAR *****************************************************/
void StopHangar(void)
{
  digitalWrite(motors1, LOW);
  digitalWrite(motors2, LOW);
}
/********************************************* LIGHTS ON *****************************************************/
void LightsOn(void)
{
  digitalWrite(lights_pin, HIGH);
}
/********************************************* LIGHTS OFF *****************************************************/
void LightsOff(void)
{
  digitalWrite(lights_pin, LOW);
}

/********************************** RECEIVE DATA FROM the APP ******************************************/
String checkClient (void)
{
  while(!client.available()) delay(1);
  String request = client.readStringUntil('\r');
  request.remove(0, 5);
  request.remove(request.length()-9,9);
  return request;
}

void connectWiFi()
{
  Serial.println("Connecting to WIFI");
  WiFi.begin(ssid, password);
  while ((!(WiFi.status() == WL_CONNECTED)))
  {
    delay(300);
    Serial.print("..");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("NodeMCU Local IP is : ");
  Serial.print((WiFi.localIP()));
}
