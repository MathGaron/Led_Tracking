#include "buttonHandler.h"
#include "pinEncoder.h"

buttonHandler powerButton(2);
buttonHandler dimButton(3);
buttonHandler blinkButton(4);

const float FREQ_HZ = 6;
const char CODE = 0xCA;

pinEncoder led(9,FREQ_HZ,CODE);
//pinEncoder ledDebugPin(13);

boolean isBlinking = false;
boolean isPowered = false;


void togglePwm(){
  byte pwm = led.getPwm();
  Serial.print("set led Pwm to:");
  Serial.println(pwm);
  switch(pwm){
  case 255: led.setPwm(100);
    break;
  case 100: led.setPwm(40);
    break;
  case 40: led.setPwm(10);
    break;
  case 10: led.setPwm(255);
    break;
  default: led.setPwm(255);
    break;
  }
  
}



void setup() {
  Serial.begin(9600);
  Serial.println("Setup Ready");
}



void loop() {
  
 if(powerButton.getRaisingEdge()){
   isPowered = !isPowered;
 } 
 if(blinkButton.getRaisingEdge()){
   isBlinking = !isBlinking;  
 }
 if(dimButton.getRaisingEdge()){
   togglePwm(); 
 }
 
 if(!isPowered){
   led.setState(OFF);
 }
 else if(isPowered && isBlinking){
   led.setState(TOGGLE);
 }
 else{
   led.setState(ON); 
 }
 
 led.update();
  
}
