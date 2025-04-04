from machine import Pin, PWM, ADC
from time import sleep

# --- Fonctions moteurs (identiques à ton code précédent) ---

def avancer(speed, speedGP, cwGP, acwGP):
    if speed > 100:
        speed = 100
    if speed < 0:
        speed = 0

    Speed = PWM(Pin(speedGP))
    Speed.freq(50)
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)

    Speed.duty_u16(int(speed / 100 * 65535))
    cw.value(1)
    acw.value(0)

def arreter(cwGP, acwGP):
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    cw.value(0)
    acw.value(0)

def avant():
    avancer(100, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    avancer(100, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def arret():
    arreter(mot1_cwPin, mot1_acwPin)
    arreter(mot2_cwPin, mot2_acwPin)

# --- Définition des broches moteurs ---
mot1_pwmPIN = 5
mot1_cwPin = 8
mot1_acwPin = 9

mot2_pwmPIN = 27
mot2_cwPin = 19
mot2_acwPin = 18

# --- Capteur de lumière ---
adc = ADC(27)  # GPIO 26

# --- Seuil de lumière à ajuster ---
seuil_lumiere = 40000  # à ajuster après test

# --- Boucle principale ---
while True:
    lumiere = adc.read_u16()
    print("Lumière =", lumiere)

    if lumiere > seuil_lumiere:
        print("→ Assez de lumière, j'avance")
        avant()
    else:
        print("→ Pas assez de lumière, je m'arrête")
        arret()

    sleep(0.5)

