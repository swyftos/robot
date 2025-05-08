#include <LiquidCrystal.h>

// LCD : RS, E, D4, D5, D6, D7
LiquidCrystal lcd(8, 9, 10, 11, 12, 13);

// Broches capteurs
const int capteur1 = A0;
const int capteur2 = A1;

// Broches LED
const int ledBas = 7;   // led bleu s'allume quand capteur bas > haut
const int ledHaut = 6;  // led rouge s'alllume quand capteur haut > bas



void setup() {
  lcd.begin(16, 2);
  lcd.clear();

  pinMode(ledBas, OUTPUT);
  pinMode(ledHaut, OUTPUT);
}

void loop() {
  int val1 = analogRead(capteur1); // A0
  int val2 = analogRead(capteur2); // A1

  float tension1 = val1 * 5.0 / 1023.0;
  float tension2 = val2 * 5.0 / 1023.0;

  // Affichage LCD
  lcd.setCursor(0, 0);
  lcd.print("A0:");
  lcd.print(val1);
  lcd.print(" ");
  lcd.print(tension1, 1);
  lcd.print("V ");

  lcd.setCursor(0, 1);
  lcd.print("A1:");
  lcd.print(val2);
  lcd.print(" ");
  lcd.print(tension2, 1);
  lcd.print("V ");

  
  if (val2 < val1) {
    digitalWrite(ledBas, HIGH);
  } else {
    digitalWrite(ledBas, LOW);
  }

  if (val2 > val1) {
    digitalWrite(ledHaut, HIGH);
  } else {
    digitalWrite(ledHaut, LOW);
  }

  delay(200);
}
