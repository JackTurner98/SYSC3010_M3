/*  Previous Version : Jack Turner December 2nd 2018
 *  Arduino main sketch for handling the hardware of the Fall 2018 SYSC3010 group M3 project. 
 *  This class acts an extention of the contrlling RPi and is always waiting for commands from it 
 *  before beginning to handle the information received
 *  Written by Maveric Garde 
 *  Version : December 3rd 2018
 */
#include <ArduinoJson.h>
#include <Time.h>
#include <TimeLib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

//Class Constants
const int OVRFLWSENSOR = 0;
const int WTRLVLSENSOR = 1;
const int TEMPSENSOR = 2;
const int FEEDERPIN = 3;


boolean feedTime = false;
boolean pushData = false;

//global data points
volatile double overFlow = 0;
volatile double waterLevel = 0;
volatile double temperature = 0;


//Global variable getter and setter functions

void setWaterLevel(double updatedData) {
  
  waterLevel = updatedData;
  
}

void setOverFlow(double updatedData) {
 /*
   * sets the global variable Overflow with the data passed tot he function
   * @param updatedData 
   */
  overFlow = updatedData;
  
}

void setTemperature(double updatedData){
  /*
   * sets the global variable Temperature with the data passed to the function 
   * @param updatedData
   */
  temperature = updatedData;
  
}


double getTemp() {
  /*
   * return the Temp as a double
   * @return temperature
   */
  return temperature;
  
}

double getOverFlow() {
  
  return overFlow;
  
}

double getWaterLevel() {
  
  return waterLevel;
  
}

void setFeed() {
  
  feedTime = true;
  
}

void setPush() {
  
  pushData = true;
  
}




int main() {

  //Arduino Main Configuration 
  pinMode(FEEDERPIN, OUTPUT); //Sets FEEDERPIN to an Output
  Serial.begin(9600); //Opens serial port at Baud rate of 9600

  
  while (!Serial) { 
    //wait for serial ports to connect
  }

  while (1) { //infinite loop logic

    char code = 'a'; //reset the code every loop to prevent false positives
    
    
    if (Serial.available() > 0) {
      //Serial Port has been written on by RPi. Decode the message
      code = (Serial.read()); //set code to the expected char code from RPi
      
      if (code == 'f') {
        //if the character sent by the RPi is f is requesting that the feeder be run
        setFeed(); //sets global variable feedTime to True
        
      }
      if (code == 'p') {
        //if the character sent by the RPi is p is requesting that new data be pushed to it. RPi will be listening 
        setPush(); //sets global variable pushData to True
      }
    }

    if (feedTime) {
      //feedTime = true feeder logic follows
      analogWrite(FEEDERPIN, HIGH);
      delay(16000); //Outputs analog high signal for 16s. Due to low amperage from the board 6s are required to begin driving the motor. This gives a 10s motor time
      analogWrite(FEEDERPIN, LOW); //Stop feeder
      feedTime = false; 
      
    }


    if (pushData) {
      //pushData = True

      //refresh all data points
      setOverFlow(analogRead(OVRFLWSENSOR));
      delay(300); //small delay to allow the circuits to settle
    
      setWaterLevel(analogRead(WTRLVLSENSOR));
      delay(300);
    
      setTemperature(analogRead(TEMPSENSOR));
      delay(300);
        
      DynamicJsonBuffer jBuffer; //Initialize a JsonBuffer Object 
      JsonObject& root = jBuffer.createObject();

      //create a 4x2 data point array to send to the RPi
      root["data"] = 1; //An expected data point requested by the RPi 
      root["Temp: "] = temperature; 
      root["Level: "] = waterLevel;
      root["Overflow: "] = overFlow;
      //send array to the RPi through the serial port
      root.prettyPrintTo(Serial);      
      pushData = false; //set pushData to False
      
    }
    
    delay(2000); //2s delay to give time for system to settle

  }


}
