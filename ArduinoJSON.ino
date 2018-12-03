#include <Time.h>
#include <TimeLib.h>
#include <ArduinoJson.h>
#include <stdio.h>
#include <stdlib.h>

// SYSC 3010 Automated Aquarium Monitoring Arduino
// Version: December 2nd 2018
// Author: John Turner

const int overflowPin = 0;
const int levelPin = 1;
const int tempPin = 2;
const int FEEDERPIN = 3;
double overFlow, waterLevel, temperature = 0;

void setup(){
  pinMode(A3, OUTPUT);
	Serial.begin(9600);
}
void feedCycle(){
  digitalWrite(A3, HIGH);
  for(int i = 0; i < 16; i++){
    delay(1000);
  }
  digitalWrite(A3, LOW);
}
void loop()

    char code = Serial.read();
    if(code == 'f'){
      feedCycle();
    }

    if(code == 'p'){
   
    	overFlow = analogRead(overflowPin); //overflow
    	waterLevel = analogRead(levelPin); //level
    	temperature = analogRead(tempPin); //temp
     
    	DynamicJsonBuffer jBuffer;
    	JsonObject& root = jBuffer.createObject();
    	
    	root["data"] = 1;
    	root["temp"] = temperature;
    	root["level"] = waterLevel;
    	root["overflow"] = overFlow;
    
      root.prettyPrintTo(Serial);
    
  }
}
