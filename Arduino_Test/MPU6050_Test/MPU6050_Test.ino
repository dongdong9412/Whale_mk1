uint8_t data[9];

float T;

float Ax;
float Ay;
float Az;

float Wx;
float Wy;
float Wz;

float Roll;
float Pitch;
float Yaw;

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(115200);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial1.available()) {
    uint8_t header = Serial1.read();
    if (header == 0x55) {
      uint8_t serviceID = Serial1.read();
//      Serial.print("Service ID: ");
//      Serial.println(serviceID, HEX);
      for (int i = 0; i < 9; i++) {
        data[i] = Serial1.read();
        delay(1);
//        Serial.print(data[i], HEX);
//        Serial.print(" ");
      }
//      Serial.println();
      if (checksum_Cal(serviceID, data)) {
        switch (serviceID) {
          case 0x51:
            acceleration_Cal(data);
            break;
          case 0x52:
            angularVelocity_Cal(data);
            break;
          case 0x53:
            angle_Cal(data);
            break;
          default:

            break;
        }
      }
      else{
        
      }
    }
  }
}
bool checksum_Cal(uint8_t serviceID, uint8_t *data) {
  uint8_t checksum;

  checksum = 0x55 + serviceID;
  for (int i = 0; i < 8; i++) {
    checksum += data[i];
  }
  if (checksum == data[8]) {
    return true;
  }
  else {
    return false;
  }
}
void acceleration_Cal(uint8_t *data) {
  Ax = (float)((data[1] << 8) | data[0]) / 32768 * 16;
  Ay = (float)((data[3] << 8) | data[2]) / 32768 * 16;
  Az = (float)((data[5] << 8) | data[4]) / 32768 * 16;
  T = (float)((data[7] << 8) | data[6]) / 340 + 36.53;
//  Serial.print("Ax: ");
  Serial.print(Ax);
  Serial.print(',');
//  Serial.print("Ay: ");
  Serial.print(Ay);
  Serial.print(',');
//  Serial.print("Az: ");
  Serial.print(Az);
  Serial.print(',');
//  Serial.print("T: ");
  Serial.println(T);
}

void angularVelocity_Cal(uint8_t *data) {
  Wx = (float)((data[1] << 8) | data[0]) / 32768 * 2000;
  Wy = (float)((data[3] << 8) | data[2]) / 32768 * 2000;
  Wz = (float)((data[5] << 8) | data[4]) / 32768 * 2000;
  T = (float)((data[7] << 8) | data[6]) / 340 + 36.53;

//  Serial.print("Wx: ");
//  Serial.println(Wx);
//  Serial.print("Wy: ");
//  Serial.println(Wy);
//  Serial.print("Wz: ");
//  Serial.println(Wz);
//  Serial.print("T: ");
//  Serial.println(T);
}

void angle_Cal(uint8_t *data) {
  Roll = (float)((data[1] << 8) | data[0]) / 32768 * 180;
  Pitch = (float)((data[3] << 8) | data[2]) / 32768 * 180;
  Yaw = (float)((data[5] << 8) | data[4]) / 32768 * 180;
  T = (float)((data[7] << 8) | data[6]) / 340 + 36.53;

//  Serial.print("Roll: ");
//  Serial.println(Roll);
//  Serial.print("Pitch: ");
//  Serial.println(Pitch);
//  Serial.print("Yaw: ");
//  Serial.println(Yaw);
//  Serial.print("T: ");
//  Serial.println(T);
}
