#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 10, 5, 4, 3, 2);

void setup() {
  // put your setup code here, to run once:
  // Serial.begin(115200);
  Serial.begin(9600);
  // Serial.println("Start...");

  lcd.begin(16,1);
  lcd.print("Scanning...");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)
  {
    String SerialData = Serial.readString();
    String CountryCode = SerialData.substring(1,5);
    String TagNumber = SerialData.substring(5,15);
    long int intCountryCode = strtol(CountryCode.c_str(), NULL, 16);
    // FUCK!!! LONG_MAX	 Maximum value for a variable of type long.	2147483647
    // Use strtoll, returns the converted integral number as a long long int value.
    // 8bit AVR not support long long int, 'strtoll' was not declared in this scope
    long long int intTagNumber = strtoll(TagNumber.c_str(), NULL, 16);

    // Serial.print("CountryCode: ");
    // Serial.println(CountryCode);
    // Serial.println(intCountryCode);
    // Serial.print("TagNumber: ");
    // Serial.println(TagNumber);
    // Serial.println(intTagNumber);

    char formatOut [16];
    sprintf (formatOut, "%04d%012lld", intCountryCode, intTagNumber);
    // Serial.print("formatOut: ");
    // Serial.println(formatOut);

    lcd.clear();
    lcd.print(formatOut);
  }
}
