import time
from machine import Pin, PWM, ADC
from BLE_SimplePeripheral import BLESimplePeripheral
import bluetooth
from time import sleep

#-------------------------fonction-moteur------------------------------------------------

#pin pour le moteur 1
mot1_pwmPIN=5
mot1_cwPin=8
mot1_acwPin=9

#pin pour le moteur 2
mot2_pwmPIN=27
mot2_cwPin=19
mot2_acwPin=18

# --- Capteurs de lumière ---
ldr_avant = ADC(2)    # GP26 (ADC0) → LDR avant
ldr_arriere = ADC(0)  # GP28 (ADC2) → LDR arrière

def avancer(speed,speedGP,cwGP,acwGP):
    if speed > 100:
        speed=100
    if speed < 0:
        speed=0
        
    Speed = PWM(Pin(speedGP))
    Speed.freq(50)
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    
    Speed.duty_u16(int(speed/100*65536))
    
    cw.value(1)
    acw.value(0)

#fait fonctionner le moteur dans le sens -1
def reculer(speed,speedGP,cwGP,acwGP):
    if speed > 100:
        speed=100
    if speed < 0:
        speed=0
        
    Speed = PWM(Pin(speedGP))
    Speed.freq(50)
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    
    Speed.duty_u16(int(speed/100*65536))
    
    cw.value(0)
    acw.value(1)

#arrete les deux moteurs
def arreter(cwGP,acwGP):
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    cw.value(0)
    acw.value(0)
    
#le sens 1 pour les 2 moteur
def avant():
    avancer(100,mot1_pwmPIN,mot1_cwPin,mot1_acwPin)
    avancer(100,mot2_pwmPIN,mot2_cwPin,mot2_acwPin)
    
#le sens -1 pour les 2 moteur
def arriere():
    reculer(100,mot1_pwmPIN,mot1_cwPin,mot1_acwPin)
    reculer(100,mot2_pwmPIN,mot2_cwPin,mot2_acwPin)
 
#le sens 1 pour le  moteur 1 et le sens -1 pour le moteur 2
def droite():
    avancer(100,mot1_pwmPIN,mot1_cwPin,mot1_acwPin)
    reculer(100,mot2_pwmPIN,mot2_cwPin,mot2_acwPin)
    
#le sens -1 pour le  moteur 1 et le sens 1 pour le moteur 2
def gauche():
    reculer(100,mot1_pwmPIN,mot1_cwPin,mot1_acwPin)
    avancer(100,mot2_pwmPIN,mot2_cwPin,mot2_acwPin)
    
#arrete les 2 moteurs
def arret():
    arreter(mot1_cwPin,mot1_acwPin)
    arreter(mot2_cwPin,mot2_acwPin)
#------------------------------------------autopilot-----------------------------------------------
def comportement_lumiere():
    seuil_detection = 30000  # Seuil minimal pour considérer que la lumière est suffisante
    while True:
        avant_val = ldr_avant.read_u16()
        arriere_val = ldr_arriere.read_u16()

        print("Avant :", avant_val, " | Arriere :", arriere_val)

        if avant_val < seuil_detection and arriere_val < seuil_detection:
            print(" Lumière trop basse → je cherche (tourner)")
            gauche(50)
        else:
            if avant_val > arriere_val:
                print(" Lumière devant → j'avance")
                avancer(70)
            else:
                print(" Lumière derrière → je recule")
                reculer(70)

        sleep(0.3)
#---------------------------------communication-------------------------------------------
led_onboard = Pin("LED", Pin.OUT)
led_onboard.off()
ble = bluetooth.BLE()
p = BLESimplePeripheral(ble,'marin')
X=''


def on_rx(v):
    global toto
    print("RX", v)
    toto=v.decode()

p.on_write(on_rx)

i = 0
toto=''
while True:
    led_onboard.on()
    if p.is_connected():
        
        '''for _ in range(3):
            data = str(i) + "_"
            print("TX", data)
            p.send(data)
        i += 1
        data =f'coucou {i}\n'
        print(data)
        p.send(data)'''
         
        X=toto
        print(X)
        
        if X =='av':
            avant()
            print('marche avant')
            p.send('marche avant')
            
            
        elif X =='ar':
            arriere()
            print('marche arriere')
            p.send('marche arriere')
             
        elif X =='dr':
            droite()
            print('tourne a droite')
            p.send('tourne a droite')
            
        elif X =='ga':
            gauche()
            print('tourne a gauche')
            p.send('tourne a gauche')
            
        elif X =='st':
            arret()
            print('arrete le moteur')
            p.send('arrete le moteur')
            
        elif X== "auto" :
            comportement_lumiere()
            print("auto on")
            p.send("auto on")
        
            
            
    else:
        led_onboard.off()
    time.sleep_ms(100)

#-----------------------------------------------------------------------------------------
