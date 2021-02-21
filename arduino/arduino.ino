//MN Maker
//Laser Temp Gun
//10.6.19

#include <Wire.h>
#include </home/pi/Desktop/arduino/sketch_jan25a/Adafruit_MLX90614.h>

const int Laser_Pin= 5;  //Laser Pin
const int echoPin = 10;
const int trigPin = 9;
const int SwitchFiveVolt = 6;
const int SwitchThreeVolt = 7;
float duration, distance;
boolean tapped = false;
boolean switchedon = false;
boolean readySignal = false;
boolean offSignal = false;
boolean onSignal = false;

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
  Serial.begin(9600);
  //Serial.println("Adafruit MLX90614 test"); 
  pinMode(trigPin, OUTPUT); // set trigpin as output
  pinMode(echoPin, INPUT); // set echopin as input
  pinMode(Laser_Pin,OUTPUT);
  pinMode(SwitchFiveVolt, OUTPUT);
  pinMode(SwitchThreeVolt, OUTPUT);

  mlx.begin(); 
  
}

float ultrasensor(){
  // clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // sets trigpin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // read echopin, return sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // calculate distance
  distance = ((duration/2) * 0.0343);
}

void loop() {
    if (Serial.available() > 0) {
    String readySignal = Serial.readString();
    if(readySignal == "SYSTEMON") {// turn on system
        digitalWrite(SwitchFiveVolt, HIGH);
        digitalWrite(SwitchThreeVolt, HIGH);
        switchedon = true;
        onSignal = false;
      }
    if(readySignal == "SYSTEMOFF") {
        digitalWrite(SwitchFiveVolt, LOW);
        digitalWrite(SwitchThreeVolt, LOW);
        switchedon = false;
        offSignal = false;
    }
    if(readySignal == "READY"){
      tapped = true;
    }
   }
  if (switchedon){
    if(readySignal) {// If it's received, 
      tapped = true; // Set tapped to true.
      //Serial.println("RECEIVED"); // And return "RECEIVED" through Serial Communication
    } else {
     Serial.println(mlx.readAmbientTempC());
     delay(5000); 
    }
    if(tapped) {// If it's ready to be tapped,   
      ultrasensor();
      while (distance > 5){
        ultrasensor();
        delay(100);
      }
      if (distance < 5){
        Serial.print(mlx.readObjectTempC());
        Serial.println();
      }
      tapped = false;
    }
  }
  
}
