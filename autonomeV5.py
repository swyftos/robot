import time
from machine import Pin, PWM, ADC
from BLE_SimplePeripheral import BLESimplePeripheral
import bluetooth
from time import sleep

#-------------------------fonction-moteur------------------------------------------------
Vitesse = 100
Seuil = 30000  # Seuil de lumière modifiable via le slider

# pin pour le moteur 1
mot1_pwmPIN = 5
mot1_cwPin = 8
mot1_acwPin = 9

# pin pour le moteur 2
mot2_pwmPIN = 27
mot2_cwPin = 19
mot2_acwPin = 18

# --- Capteurs de lumière ---
ldr_avant = ADC(2)    # GP28 (ADC2) → LDR avant
ldr_arriere = ADC(0)  # GP26 (ADC0) → LDR arrière

def avancer(speed, speedGP, cwGP, acwGP):
    if speed > 100:
        speed = 100
    if speed < 0:
        speed = 0
    Speed = PWM(Pin(speedGP))
    Speed.freq(50)
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    Speed.duty_u16(int(speed / 100 * 65536))
    cw.value(1)
    acw.value(0)

def reculer(speed, speedGP, cwGP, acwGP):
    if speed > 100:
        speed = 100
    if speed < 0:
        speed = 0
    Speed = PWM(Pin(speedGP))
    Speed.freq(50)
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    Speed.duty_u16(int(speed / 100 * 65536))
    cw.value(0)
    acw.value(1)

def arreter(cwGP, acwGP):
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    cw.value(0)
    acw.value(0)

def avant():
    avancer(Vitesse, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    avancer(Vitesse, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def arriere():
    reculer(Vitesse, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    reculer(Vitesse, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def droite():
    avancer(Vitesse, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    reculer(Vitesse, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def gauche():
    reculer(Vitesse, mot1_pwmPIN, mot1_cwPin, mot1_acwPin)
    avancer(Vitesse, mot2_pwmPIN, mot2_cwPin, mot2_acwPin)

def arret():
    arreter(mot1_cwPin, mot1_acwPin)
    arreter(mot2_cwPin, mot2_acwPin)

#------------------------------------------autopilot-----------------------------------------------
def comportement_lumiere():
    global Seuil
    while True:
        avant_val = ldr_avant.read_u16()
        arriere_val = ldr_arriere.read_u16()

        print("Avant :", avant_val, " | Arrière :", arriere_val, " | Seuil :", Seuil)

        if avant_val < Seuil and arriere_val < Seuil:
            print("Lumière trop basse → je cherche (tourner)")
            gauche()
        else:
            if avant_val > arriere_val:
                print("Lumière devant → j'avance")
                avant()
            else:
                print("Lumière derrière → je recule")
                arriere()

        sleep(0.3)

#---------------------------------communication-------------------------------------------
led_onboard = Pin("LED", Pin.OUT)
led_onboard.off()

ble = bluetooth.BLE()
p = BLESimplePeripheral(ble, 'marin')

toto = ''
X = ''

def on_rx(v):
    global toto
    print("RX", v)
    toto = v.decode().strip()

p.on_write(on_rx)

while True:
    led_onboard.on()
    if p.is_connected():
        X = str(toto)
        print("Valeur reçue :", X)

        if X == 'av':
            avant()
            print("marche avant")
            p.send("marche avant")

        elif X == 'de':
            arriere()
            print("marche arrière")
            p.send("marche arrière")

        elif X == 'dr':
            droite()
            print("tourne à droite")
            p.send("tourne à droite")

        elif X == 'ga':
            gauche()
            print("tourne à gauche")
            p.send("tourne à gauche")

        elif X == 'stop':
            arret()
            print("arrêt du moteur")
            p.send("moteur arrêté")

        elif X == "auto":
            print("mode automatique")
            p.send("mode auto activé")
            comportement_lumiere()

        else:
            try:
                valeur = int(X)
                if 0 <= valeur <= 100:
                    Vitesse = valeur
                    print("Vitesse ajustée à :", Vitesse)
                    p.send("Vitesse = " + str(Vitesse))
                elif 10000 <= valeur <= 65535:
                    Seuil = valeur
                    print("Seuil lumière ajusté à :", Seuil)
                    p.send("Seuil lumière = " + str(Seuil))
                else:
                    print("Valeur hors plage :", valeur)
            except:
                print("Commande invalide :", X)

    else:
        led_onboard.off()

    time.sleep_ms(100)
