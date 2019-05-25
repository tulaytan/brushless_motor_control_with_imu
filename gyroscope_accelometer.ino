// Bu kütüphane I2C Haberleşmesine izin veriyor.
#include <Wire.h>

// MPU-6050'nin I2C adresi
const int MPU_ADDR = 0x68;
// AD0 pini;
// I2C adresi LOW ve HIGH durumuna göre değişir
// LOW ---- > 0X68 HIGH ----> 0X69


// İvmeölçer için değişken raw datası
int16_t accelerometer_x, accelerometer_y, accelerometer_z;
 
// Jiroskop için değişken raw datası
int16_t gyro_x, gyro_y, gyro_z; 

// Sıcaklık için değişken datası
int16_t temperature;

char tmp_str[7]; // temporary variable used in convert function

// 16 bitlik int tipindeki değişkeni string olarak döndüren fonksiyon
char* convert_int16_to_str(int16_t i) 
{ 
  sprintf(tmp_str, "%6d", i);
  return tmp_str;
}
void setup() {
  Serial.begin(9600);
  Wire.begin();
  // I2C slave cihazına aktarım başlar (GY-521 board)
  Wire.beginTransmission(MPU_ADDR);
  // PWR_MGMT_1 register
  Wire.write(0x6B); 
  // 0 olarak set eder MPU-6050'yi uyandırır
  Wire.write(0);
  Wire.endTransmission(true);
}

void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  // 7*2 = 14 registar'a istek yapılır
  Wire.requestFrom(MPU_ADDR, 7*2, true);

  // "Wire.read() << 8 | Wire.read();" 
  // Anlamı 2 register aynı değişkende okuma ve depolama yapılır
  
  // Registerlar okunur: 0x3B (ACCEL_XOUT_H) ve 0x3C (ACCEL_XOUT_L)
  accelerometer_x = Wire.read()<<8 | Wire.read();
  // Registerlar okunur: 0x3D (ACCEL_YOUT_H) ve 0x3E (ACCEL_YOUT_L)
  accelerometer_y = Wire.read()<<8 | Wire.read();
  // Registerlar okunur: 0x3F(ACCEL_ZOUT_H) ve 0x40 (ACCEL_ZOUT_L)
  accelerometer_z = Wire.read()<<8 | Wire.read();

  // Registerlar okunur: 0x41 (TEMP_OUT_H) ve 0x42 (TEMP_OUT_L)
  temperature = Wire.read()<<8 | Wire.read();
  
  // Registerlar okunur: 0x43 (GYRO_XOUT_H) ve 0x44 (GYRO_XOUT_L)
  gyro_x = Wire.read()<<8 | Wire.read(); 
  // Registerlar okunur: 0x43 (GYRO_XOUT_H) ve 0x44 (GYRO_XOUT_L)
  gyro_y = Wire.read()<<8 | Wire.read();
  // Registerlar okunur: 0x43 (GYRO_XOUT_H) ve 0x44 (GYRO_XOUT_L)
  gyro_z = Wire.read()<<8 | Wire.read(); 
  
  // Dataların ekrana bastırılması
  // İvmeölçer datalarının bastırılması
  Serial.print("aX: ");
  Serial.print(convert_int16_to_str(gyro_x));
  Serial.print("  aY: ");
  Serial.print(convert_int16_to_str(gyro_y));
  Serial.print("  aZ: ");
  Serial.print(convert_int16_to_str(gyro_z));


  // Jiroskop datalarının bastırılması
  Serial.print("  gX: ");
  Serial.print(convert_int16_to_str(accelerometer_x));
  Serial.print("  gY: ");
  Serial.print(convert_int16_to_str(accelerometer_y));
  Serial.print("  gZ: ");
  Serial.print(convert_int16_to_str(accelerometer_z));

  // Sıcaklık datasının bastırılması
  Serial.print(" Sıcaklık: ");
  Serial.print(temperature/340.00+36.53);

  Serial.println();
  
  // delay
  delay(1000);
}
