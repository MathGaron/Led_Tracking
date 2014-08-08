/*
    Simple class to manipulate button with pull down resistor. It return true if a raising edge was detected while polling.
    It include a software debouncer
    
    by: Mathieu Garon  mathieugaron91@gmail.com
*/

#ifndef _BUTTONHANDLER_H
#define _BUTTONHANDLER_H


#include "Arduino.h"

class buttonHandler{
  public:
    buttonHandler(int pin, int debounceDelay=50);
    
    boolean getRaisingEdge();
    
  private:
    int mPin;
    int mLastButtonState;
    int mDebounceDelay;
    int mLastDebounceTime;
  
};

#endif
