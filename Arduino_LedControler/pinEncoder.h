/*
    Class that manipulate a pin (for now analog only) to 3 states : ON, OFF (wich are self explanatory) and TOGGLE:
    Toggle will switch state of the pin at a given frequency with a binary code.
    
    by: Mathieu Garon  mathieugaron91@gmail.com
*/

#ifndef _PINENCODER_H
#define _PINENCODER_H

#define DEBUG

#include "Arduino.h"
#include "rol.h"

typedef enum state {
  OFF,
  ON,
  TOGGLE
} state;

class pinEncoder{
  public:
    pinEncoder(int iPin, float iFrequency=1, char iCode = 0xAA, byte iPwm = 255);  //default code in binary : 10101010
    
    void setPwm(byte iPwm);
    byte getPwm();
    void setFrequency(float iFrequency);
    void setState(state iState);

    void update();
  
  private:

    float frequencyToMilliseconds(float hz);
    void setPin();

    int mPin;
    float mTimeGap;  //ms
    rol mCode;
    byte mPwm;
    state mState;
    
    
    
    long mLastUpdateTime; 
  
};

inline void pinEncoder::setPwm(byte iPwm){
  mPwm = iPwm; 
}

inline byte pinEncoder::getPwm(){
  return mPwm; 
}

inline void pinEncoder::setFrequency(float iFrequency){
  mTimeGap = this->frequencyToMilliseconds(iFrequency);
}

inline void pinEncoder::setState(state iState){
  mState = iState;
}

inline float pinEncoder::frequencyToMilliseconds(float hz){
  return (1/hz)*1000;
}

inline void pinEncoder::setPin(){
  int lsb = mCode.getByte() & 0x01;
  if(lsb){
    analogWrite(mPin,mPwm);
#ifdef DEBUG
    digitalWrite(13,HIGH);
#endif
  }
  else{
    analogWrite(mPin,0);
#ifdef DEBUG
    digitalWrite(13,LOW);
#endif
  }
}


#endif
