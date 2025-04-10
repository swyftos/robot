from machine import Pin, PWM
from time import sleep


def motorMove(speed,direction,speedGP,cwGP,acwGP):
   if speed > 100:
       speed=100
   if speed < 0:
       speed=0
       

   
   Speed = PWM(Pin(speedGP))
   Speed.freq(50)
   cw = Pin(cwGP, Pin.OUT)
   acw = Pin(acwGP, Pin.OUT)
   
   Speed.duty_u16(int(speed/100*65536))
   
   if direction < 0:
     cw.value(0)
     acw.value(1)
     
   if direction == 0:
     cw.value(0)
     acw.value(0)
     
   if direction > 0:
     cw.value(1)
     acw.value(0)


   
#pin pour le moteur 1
mot1_pwmPIN=5
mot1_cwPin=8
mot1_acwPin=9

#pin pour le moteur 2
mot2_pwmPIN=27
mot2_cwPin=19
mot2_acwPin=18

 

v=0
#fait varier les moteurs dans les 2 sens
#for v in range(100):
#    motorMove(v,1,mot1_pwmPIN,mot1_cwPin,mot1_acwPin)
#    motorMove(v,1,mot2_pwmPIN,mot2_cwPin,mot2_acwPin)
#    sleep(0.1)

#for v in range(100,0,-1):
#    motorMove(v,1,mot1_pwmPIN,mot1_cwPin,mot1_acwPin)
#    motorMove(v,1,mot2_pwmPIN,mot2_cwPin,mot2_acwPin)
#    sleep(0.1)

#fait fonctionner le moteur dans le sens 1
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
   
def arret():
   arreter(mot1_cwPin,mot1_acwPin)
   arreter(mot2_cwPin,mot2_acwPin)

avant()
sleep(2)
arriere()
sleep(2)
droite()
sleep(2)
gauche()
sleep(2)
arret()
 
