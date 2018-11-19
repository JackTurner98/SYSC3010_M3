// ArduinoJson - Version: 5.13.3
#include <ArduinoJson.h>

int overflowPin = 0;
int levelPin = 1;
int tempPin = 2;

void setup(){
	Serial.begin(9600);
}

void loop(){
  if (Serial.read() == '1'){
  	float overFlowVal = analogRead(overflowPin); //overflow
   
  	float waterLevelVal = analogRead(levelPin); //level
   
  	float tempVal = analogRead(tempPin); //temp
     
  	DynamicJsonBuffer jBuffer;
  	JsonObject& root = jBuffer.createObject();
  	
  	root["data"] = 1;
  	root["temp"] = tempVal;
  	root["level"] = waterLevelVal;
  	root["overflow"] = overFlowVal;
  
    root.prettyPrintTo(Serial);
  }
}
