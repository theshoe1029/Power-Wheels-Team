#include <Servo.h>

Servo steeringServo;
Servo throttleServo;

void setup() 
{
  Serial.begin(115200);
  steeringServo.attach(9);
  throttleServo.attach(10);
}

void loop() 
{
  if(Serial.available())
  {
    char ch;
    int num;
    String input = Serial.readStringUntil('\n');
    sscanf((const char*)input.c_str(), "%c%d", &ch, &num);
    if(ch=='S'){steeringServo.write(num);}
    if(ch=='T'){throttleServo.write(num);}
  }
}





