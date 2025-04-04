from machine import Pin, PWM, ADC
from time import sleep

# --- Fonctions moteurs avec vitesse variable ---
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

# --- Boucle principale ---
while True:
    lumiere = adc.read_u16()
    volt = 3.3 * (lumiere / 65535)
    print("Lumière =", lumiere, "→ {:.2f} V".format(volt))

    if lumiere > 60000:
        print("→ Lumière forte, j'arrête")
        arret()
    elif lumiere > 40000:
        print("→ Lumière moyenne, j'avance doucement")
        avancer(30)
    elif lumiere > 20000:
        print("→ Lumière faible, j'avance normalement")
        avancer(60)
    else:
        print("→ Obscurité totale, j'avance vite !")
        avancer(100)

    sleep(0.5)
