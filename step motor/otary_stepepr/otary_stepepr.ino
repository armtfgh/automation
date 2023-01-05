volatile byte i=0;
volatile int Signal;
volatile int inByte;

String inputString = "";         // a string to hold incoming data // Valve control
boolean stringComplete = false;  // whether the string is complete

int driverPUL = 13;    // PUL- pin
int driverDIR = 12;    // DIR- pin
String sub;


String readString;
int pd = 50;
int movement;
//int movem = -31000;

void setup() {
  Serial.begin(9600);
  
  pinMode (driverPUL, OUTPUT);  //for Sampler
  pinMode (driverDIR, OUTPUT);
  Serial.println("Step Motor Revolution"); 

}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    readString += c;
    sub = readString.substring(0,1);
    delay(2);
  }

  


     
  if (readString.length() >0 && sub.equals("u")){
    Serial.println(readString);
    int n = readString.substring(1).toInt();
    Serial.println(n);
  
    for (int i=0; i<n; i++)  // 9
     {
      digitalWrite(driverDIR,LOW);
      digitalWrite(driverPUL,HIGH);
      delayMicroseconds(pd);
      digitalWrite(driverPUL,LOW);
      delayMicroseconds(pd);
     }
     readString="";
     delay(10);
  }

       
  if (readString.length() >0 && sub.equals("d")){
    Serial.println(readString);
    int n = readString.substring(1).toInt();
    Serial.println(n);
  
    for (int i=0; i<n; i++)  // 9
     {
      digitalWrite(driverDIR,HIGH);
      digitalWrite(driverPUL,HIGH);
      delayMicroseconds(pd);
      digitalWrite(driverPUL,LOW);
      delayMicroseconds(pd);
     }
     readString="";
     delay(10);
  }
  

  
}
//  }
//
//  if(Signal==16)  // 10 in MATLAB, digit
//
//  {
//  for (int i=0; i<movement; i++)
//   {
//    digitalWrite(driverDIR,HIGH);
//    digitalWrite(driverPUL,HIGH);
//    delayMicroseconds(pd);
//    digitalWrite(driverPUL,LOW);
//    delayMicroseconds(pd);
//   }
//   Signal=17;
//   delay(10);
//  }
//}
