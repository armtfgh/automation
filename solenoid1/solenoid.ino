volatile byte i=0;
volatile int Signal;
volatile int inByte;

String inputString = "";         // a string to hold incoming data // MATLAB과 serial 통신 통한 Valve control
boolean stringComplete = false;  // whether the string is complete


const int analogInPin = A1;  //
int sensorValue = 0;  


// the setup function runs once when you press reset or power the board
void setup() {

Serial.begin(9600);
 
pinMode(2, OUTPUT);
pinMode(3, OUTPUT);
pinMode(4, OUTPUT);
pinMode(6, OUTPUT);

}

// the loop function runs over and over again forever
void loop() {

  if (stringComplete)
  {  // print the string when a newline arrives:
        Signal = (int)strtol(&inputString[0], NULL, 16);
        Serial.println(Signal);
        inputString = "";  // clear the string:
        stringComplete = false;  //go to read Serial
  }
   
  if(Signal==1)
  {
    digitalWrite(2, HIGH);  
  }  
  if(Signal==2)
  {
    digitalWrite(3, HIGH);  
  }  
  if(Signal==3)
  {
    digitalWrite(4, HIGH);  
  }  
    if(Signal==8)
  {
    digitalWrite(6, HIGH);  
  }  
 
 
  if(Signal==5)
  {
    digitalWrite(2, LOW);  
  }  
  if(Signal==6)
  {
    digitalWrite(3, LOW);  
  }  
  if(Signal==7)
  {
    digitalWrite(4, LOW);  
  }
   if(Signal==9)
  {
    digitalWrite(6, LOW);  
  }    
  
}

void serialEvent()
{
    while (Serial.available())
    {
        char inChar = (char)Serial.read();
        inputString+=inChar;
        if (inChar == '#')
        {
          stringComplete = true;
        }
    }
}
