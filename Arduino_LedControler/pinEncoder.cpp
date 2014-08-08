#include "pinEncoder.h"

pinEncoder::pinEncoder(int iPin, float iFrequency, char iCode, byte iPwm):mPin(iPin),mCode(iCode), mPwm(iPwm),mState(OFF){
  pinMode(mPin,OUTPUT);
#ifdef DEBUG
  pinMode(13,OUTPUT);
#endif
  mTimeGap = this->frequencyToMilliseconds(iFrequency);
  mLastUpdateTime = millis();
}

void pinEncoder::update(){
  if(mState == OFF){
    analogWrite(mPin,0);
#ifdef DEBUG
    digitalWrite(13,LOW);  
#endif

  }
  else if(mState == ON){
    
    analogWrite(mPin,mPwm);
#ifdef DEBUG
    digitalWrite(13,HIGH);
#endif

  }
  else if(mState == TOGGLE){
    long delta =millis() - mLastUpdateTime;
    if(delta > mTimeGap){
      mLastUpdateTime = millis();
      mCode.rollRight();
    }
    this->setPin();
  }
  
}
