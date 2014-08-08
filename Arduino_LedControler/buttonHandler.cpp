#include "buttonHandler.h"

buttonHandler::buttonHandler(int pin, int debounceDelay):mPin(pin),mDebounceDelay(debounceDelay),
mLastDebounceTime(0){
  pinMode(mPin,INPUT);
  mLastButtonState = digitalRead(mPin);
}

boolean buttonHandler::getRaisingEdge(){
  int state = digitalRead(mPin);
  boolean raisingEdge = false;
  if(state != mLastButtonState){
    mLastDebounceTime = millis();
  }
  if((millis()-mLastDebounceTime) > mDebounceDelay){
    if(mLastButtonState == LOW && state == HIGH){
      raisingEdge = true; 
    }
  }
  
  mLastButtonState = state;
  return raisingEdge;
  
}
