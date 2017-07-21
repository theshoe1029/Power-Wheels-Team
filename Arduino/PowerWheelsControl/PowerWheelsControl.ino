#include <Servo.h>

Servo steerServo;
Servo throttleServo;
unsigned long throttleTimer;
int steeringPin = 9;
int throttlePin = 10;
int lastThrottle = 0;
String input;
String commands[2];
String params[2];
int intParams[2];
int commaIndex;
int epsilon = 35;
bool activateRadio = false;
int radioThrottle;
int radioTurn;
int radioAngle = 0;
int toggle;
int currentState;
int mode = 0;
bool activateSerial = false;


void stoppy()
{
  throttleServo.write(90);
}

double scaleRadioThrottle(int speed)
{
  double adjustedSpeed = map(speed, 1100, 2000, 0, 180);
  return adjustedSpeed;
}

double scaleRadioTurn(int angle)
{
  double adjustedAngle = map(angle, 1200, 1775, 75, 115);
  return adjustedAngle;
}

double scaleThrottle(int speed)
{
  double adjustedSpeed = map(speed, -100, 100, 0, 180);
  return adjustedSpeed;
}

double scaleSteering(double angle)
{
  double adjustedAngle = map(angle, -90, 90, 0, 180);
  return adjustedAngle;
}

void timeThrottle(int speed, int time)
{
  double adjustedSpeed = scaleThrottle(speed);
  throttleServo.write(adjustedSpeed);
  delay(time);
  stoppy();
}

void throttle(int speed)
{
  double adjustedSpeed = scaleThrottle(speed);
  throttleServo.write(adjustedSpeed);
}

void turn(int angle)
{
  double adjustedAngle = scaleSteering(angle);
  steerServo.write(adjustedAngle);
}

void resetSerial()
{
  input = "";
  commaIndex = 0;
  commands[0] = "";
  commands[1] = "";
  params[0] = "";
  params[1] = "";
}

void detectToggle()
{
  toggle = pulseIn(A0, HIGH, 25000);
  if (toggle < 1250)
    mode = 0;
  else
    mode = 1;
}

void autonomous()
{
  Serial.println("You ran auto");
}

void serialEvent()
{
  if (activateSerial) {
    //detectToggle();
    resetSerial();
    if (Serial.available())
    {
      char ch;
      int num;
      
      resetSerial();
      //detectToggle();
      input = Serial.readStringUntil('\n');
      sscanf((const char*)input.c_str(), "%c%d", &ch, &num);
      steerServo.write(num);
      /*for (int i = 0; i < input.length(); i ++)
      {
        if (isAlpha(input.charAt(i)))
          commands[0] += input[i];
        else
          commands[1] += input[i];
      }
      for (int i = 0; i < commands[1].length(); i ++)
      {
        if (isPunct(commands[1].charAt(i)))
          commaIndex = i;
      }

      if (commaIndex == 0)
        commaIndex = 10;

      for (int i = 0; i < commaIndex; i ++)
        params[0] += commands[1].charAt(i);
      for (int i = commaIndex + 1; i < commands[1].length(); i ++)
        params[1] += commands[1].charAt(i);

      intParams[0] = params[0].toInt();
      intParams[1] = params[1].toInt();/*
      
      /*resetSerial();
      detectToggle();
      input = Serial.readStringUntil("\n");
      for (int i = 0; i < input.length(); i ++)
      {
        if (isAlpha(input.charAt(i)))
          commands[0] += input[i];
        else
          commands[1] += input[i];
      }
      for (int i = 0; i < commands[1].length(); i ++)
      {
        if (isPunct(commands[1].charAt(i)))
          commaIndex = i;
      }

      if (commaIndex == 0)
        commaIndex = 10;

      for (int i = 0; i < commaIndex; i ++)
        params[0] += commands[1].charAt(i);
      for (int i = commaIndex + 1; i < commands[1].length(); i ++)
        params[1] += commands[1].charAt(i);

      intParams[0] = params[0].toInt();
      intParams[1] = params[1].toInt();*/

      /*if (commands[0] != "")
        Serial.print(commands[0]);
      if (params[0] != "")
        Serial.print(params[0]);
      if (params[1] != "")
        Serial.print(params[1]);
      Serial.println();*/
    }

    /*if (commands[0] == "radio")
      activateRadio = true;

    if (commands[0] == "stopradio")
      activateRadio = false;

    //Motors run forever at set speed
    if (commands[0] == "m")
      throttle(intParams[0]);

    //Motors run for time at set speed
    if (commands[0] == "mt")
    {
      timeThrottle(intParams[0], intParams[1]);
      resetSerial();
    }

    //Stop robot
    if (commands[0] == "s")
      stoppy();

    if (commands[0] == "run")
      autonomous();*/

    //Turn wheels at angle
    //if (commands[0] == "t")turn(intParams[0]);
  }
}

void radioEvent()
{
  if (activateRadio)
  {
    detectToggle();
    radioThrottle = pulseIn(6, HIGH, 25000);
    radioTurn = pulseIn(7, HIGH, 25000);

    double scaledRadioThrottle = scaleRadioThrottle(radioThrottle);
    double scaledRadioTurn = scaleRadioTurn(radioTurn);

    if (radioThrottle < (1505 - epsilon))
      throttleServo.write(scaledRadioThrottle);
    if (radioThrottle > (1525 + epsilon))
      throttleServo.write(scaledRadioThrottle);
    if (radioThrottle < (1525 + epsilon) && radioThrottle > (1505 - epsilon))
      throttle(0);

    steerServo.write(scaledRadioTurn);
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  steerServo.attach(9);
  throttleServo.attach(10);
  turn(0);
  throttleServo.write(90);
  Serial.println("Serial is ready");
  Serial.println("Commands: m-run motors, mt-run motors for time, t-turn wheels, s-stop motors");
  Serial.println("Please enter command...");
}

void loop() {
  // put your main code here, to run repeatedly:
  //detectToggle();
  //radioEvent();
  serialEvent();
  if (mode == 0)
  {
    activateSerial = true;
    activateRadio = false;
  }
  else
  {
    activateRadio = true;
    activateSerial = false;
  }
}
