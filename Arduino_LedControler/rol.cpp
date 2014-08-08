#include "rol.h"

rol::rol(byte iByte):mByte(iByte){
   
}


void rol::rollLeft(){
  byte msb = mByte & 0x80;
  mByte <<= 1;
  mByte |= (msb >> 7);
}

void rol::rollRight(){
  byte lsb = mByte & 0x01;   //keep rightmost byte
  mByte >>= 1;              //shift
  mByte |= (lsb << 7);       //update msb
}
