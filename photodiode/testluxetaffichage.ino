#include <LiquidCrystal.h>

// LCD : RS, E, D4, D5, D6, D7
LiquidCrystal lcd(8, 9, 10, 11, 12, 13);

const int capteur1 = A0;
const int capteur2 = A1;

void setup() {
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Capteurs Lumiere");
}

void loop() {
  int val1 = analogRead(capteur1);
  int val2 = analogRead(capteur2);

  float tension1 = val1 * 5.0 / 1023.0;
  float tension2 = val2 * 5.0 / 1023.0;

  // Ligne 1 : capteur 1
  lcd.setCursor(0, 0);
  lcd.print("A0:");
  lcd.print(val1);
  lcd.print(" ");
  lcd.print(tension1, 1); // 1 chiffre après virgule
  lcd.print("V");

  // Ligne 2 : capteur 2
  lcd.setCursor(0, 1);
  lcd.print("A1:");
  lcd.print(val2);
  lcd.print(" ");
  lcd.print(tension2, 1);
  lcd.print("V");

  delay(500);
}
