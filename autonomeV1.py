from machine import Pin, PWM, ADC
from time import sleep

# --- Fonctions moteurs ---
def avancer(vitesse):
    avancerMoteur(vitesse, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    avancerMoteur(vitesse, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def avancerMoteur(speed, speedGP, cwGP, acwGP):
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

def tourner_gauche(vitesse):
    avancerMoteur(0, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)      # Moteur gauche à l'arrêt
    avancerMoteur(vitesse, mot2_pwmPIN, mot2_cwPin, mot2_acwPin) # Moteur droit avance

def arret():
    arreter(mot1_cwPin, mot1_acwPin)
    arreter(mot2_cwPin, mot2_acwPin)

def arreter(cwGP, acwGP):
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    cw.value(0)
    acw.value(0)

# --- Brochage des moteurs ---
mot1_pwmPIN = 5
mot1_cwPin = 8
mot1_acwPin = 9

mot2_pwmPIN = 27
mot2_cwPin = 19
mot2_acwPin = 18

# --- Capteur de lumière ---
adc = ADC(26)

# --- Fonction de recherche de lumière ---
def rechercher_lumiere():
    while True:
        lumiere = adc.read_u16()
        volt = 3.3 * (lumiere / 65535)
        print("Lumière =", lumiere, "→ {:.2f} V".format(volt))

        if lumiere > 60000:
            print( Lumière détectée ! J'avance vers elle")
            avancer(80)
        else:
            print( Je cherche la lumière (rotation...)")
            tourner_gauche(40)

        sleep(0.3)

# --- Boucle principale ---
rechercher_lumiere()

