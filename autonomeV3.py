from machine import Pin, PWM, ADC
from time import sleep

# --- Brochage des moteurs ---
mot1_pwmPIN = 5
mot1_cwPin = 8
mot1_acwPin = 9

mot2_pwmPIN = 27
mot2_cwPin = 19
mot2_acwPin = 18

# --- Capteurs de lumière ---
ldr_avant = ADC(2)    # GP26 (ADC0) → LDR avant
ldr_arriere = ADC(0)  # GP28 (ADC2) → LDR arrière

# --- Fonctions moteurs ---
def avancerMoteur(speed, speedGP, cwGP, acwGP):
    speed = max(0, min(speed, 100))
    Speed = PWM(Pin(speedGP))
    Speed.freq(50)
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    Speed.duty_u16(int(speed / 100 * 65535))
    cw.value(1)
    acw.value(0)

def reculerMoteur(speed, speedGP, cwGP, acwGP):
    speed = max(0, min(speed, 100))
    Speed = PWM(Pin(speedGP))
    Speed.freq(50)
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    Speed.duty_u16(int(speed / 100 * 65535))
    cw.value(0)
    acw.value(1)

def arreter(cwGP, acwGP):
    Pin(cwGP, Pin.OUT).value(0)
    Pin(acwGP, Pin.OUT).value(0)

def avancer(speed):
    avancerMoteur(speed, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    avancerMoteur(speed, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def reculer(speed):
    reculerMoteur(speed, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    reculerMoteur(speed, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def tourner_gauche(speed):
    avancerMoteur(0, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    avancerMoteur(speed, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def tourner_droite(speed):
    avancerMoteur(speed, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    avancerMoteur(0, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def arret():
    arreter(mot1_cwPin, mot1_acwPin)
    arreter(mot2_cwPin, mot2_acwPin)

# --- Recherche et réaction à la lumière ---
def comportement_lumiere():
    seuil_detection = 30000  # Seuil minimal pour considérer que la lumière est suffisante
    while True:
        avant_val = ldr_avant.read_u16()
        arriere_val = ldr_arriere.read_u16()

        print("Avant :", avant_val, " | Arrière :", arriere_val)

        if avant_val < seuil_detection and arriere_val < seuil_detection:
            print(" Lumière trop basse → je cherche (tourner)")
            tourner_gauche(20)
        else:
            if avant_val > arriere_val:
                print(" Lumière devant → j'avance")
                avancer(50)
            else:
                print(" Lumière derrière → je recule")
                reculer(50)

        sleep(0.3)

# --- Lancement du programme ---
comportement_lumiere()

