const int pin_heater = 4; //ヒーター電源
const int pin_senser_on = 3; //センサー電源
const int pin_senser = A0; //センサー

 

/*初期設定*/

void setup(){

  //センサーとヒーター電源をアウトプット宣言
  pinMode(pin_senser_on,OUTPUT);
  pinMode(pin_heater,OUTPUT);

  //センサーとヒーターの出力をOFF
  digitalWrite(pin_senser_on, LOW);
  digitalWrite(pin_heater, LOW);

  //シリアル出力設定
  Serial.begin(115200);
}

 

/*センサーの値を読む*/

int readSenser(){
  int val = 0;

  //センサー電源ON
  digitalWrite( pin_senser_on, HIGH );
  delay( 5 ); //一応待つ
  val = analogRead( pin_senser );//読む

  //センサー電源OFF
  digitalWrite( pin_senser_on, LOW );
  return val;//取得値を返す

}

 

/*ヒーターの過熱*/

void heat(){

  //8ms過熱
  digitalWrite( pin_heater, HIGH );
  delay( 8 );

  //237ms冷却
  digitalWrite( pin_heater, LOW );
  delay( 237 );
}

 

/*メインルーチン*/

void loop(){
  int val = 0;
  //臭いに反応したら数値が上がるように、取得値を逆転させる
  val = 1023 - readSenser();
  for(int i=0;i<4;i++){
    heat();
  }
  Serial.println(val);
}
