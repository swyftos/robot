from machine import Pin, PWM, ADC
from time import sleep

# --- Fonctions moteurs ---
def avancer(vitesse):
    avancerMoteur(vitesse, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    avancerMoteur(vitesse, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def avancerMoteur(speed, speedGP, cwGP, acwGP):
    speed = max(0, min(speed, 100))  # Clamp entre 0 et 100

    Speed = PWM(Pin(speedGP))
    Speed.freq(50)
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)

    Speed.duty_u16(int(speed / 100 * 65535))
    cw.value(1)
    acw.value(0)

def tourner_gauche(vitesse):
    avancerMoteur(0, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)       # Stop gauche
    avancerMoteur(vitesse, mot2_pwmPIN, mot2_cwPin, mot2_acwPin) # Droit avance

def tourner_droite(vitesse):
    avancerMoteur(vitesse, mot1_pwmPIN, mot1_cwPin, mot1_acwPin) # Gauche avance
    avancerMoteur(0, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)       # Stop droit

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

# --- Capteurs de lumière ---
ldr_avant = ADC(0)  # GP26 = ADC0
ldr_arriere = ADC(2)  # GP28 = ADC2

# --- Fonction de recherche de lumière ---
def rechercher_lumiere():
    while True:
        val_avant = ldr_avant.read_u16()
        val_derrière = ldr_arriere.read_u16()

        print("devant :", ldr_avant, " | derriere :", ldr_arriere)

        if abs(val_avant > val_derrière) :
            print("→ Lumière en face : j'avance")
            avancer(80)
        elif val_derrière > val_avant:
            print("→ Lumière derrière : je tourne à gauche")
            tourner_gauche(50)
        else:
            print("→ Lumière à droite : je tourne à droite")
            tourner_droite(50)

        sleep(0.3)

# --- Lancement ---
rechercher_lumiere()
