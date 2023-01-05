#include <movingAvg.h>
const int inp = A1;
const int sdelay = 10;
movingAvg mySensor(40); 



void setup() {
  // put your setup code here, to run once:
  pinMode(inp,INPUT);
  Serial.begin(9600);
  mySensor.begin();


}

void loop() {
  // put your main code here, to run repeatedly:
  int val = analogRead(inp);
  int avg = mySensor.reading(val);
//  Serial.print(0);
//  Serial.print(" ");  
//  Serial.print(10000);
//  Serial.print(" ");
  int res = map(avg,300,1024,0,9800);
  Serial.println(res);
//  Serial.print(" ");
  delay(sdelay);

}
