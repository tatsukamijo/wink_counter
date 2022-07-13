void setup() {
  // put your setup code here, to run once:
  pinMode(13,OUTPUT);
  Serial.begin(9600);

}

byte inputData;
void loop() {
  // シリアルデータを受信したら処理を実行する
  if (Serial.available() > 0) {
    inputData = Serial.read();
    switch(inputData){
      case '1':
      for (int i = 0; i<100; i++){
        digitalWrite(13, HIGH);
        delay(50);
        digitalWrite(13,LOW);
        delay(50);
      }
    }
  }
}
