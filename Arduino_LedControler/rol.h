/*
    This small class simply encapsulate a byte (can be extended to an array later) and add bit rolling
    functions.
    
    by: Mathieu Garon  mathieugaron91@gmail.com
*/


#ifndef _ROL_H
#define _ROL_H

#include "Arduino.h"

class rol{
  public:
    rol(byte iByte);
    
    void setByte(byte iByte);
    byte getByte();
    
    void rollLeft();
    void rollRight();
  
  private:
    byte mByte;
  
};

inline void rol::setByte(byte iByte){
  mByte = iByte;
}

inline byte rol::getByte(){
  return mByte; 
}

#endif
