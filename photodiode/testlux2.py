from machine import ADC
import time

ldr1 = ADC(0)  # ADC0 = GP26
ldr2 = ADC(2)  # ADC2 = GP28

while True:
    valeur1 = ldr1.read_u16()
    valeur2 = ldr2.read_u16()

    tension1 = 3.3 * (valeur1 / 65535)
    tension2 = 3.3 * (valeur2 / 65535)

    print("LDR Avant  :", valeur1, "→ {:.2f} V".format(tension1))
    print("LDR Arrière:", valeur2, "→ {:.2f} V".format(tension2))
    print("-" * 40)

    time.sleep(1)
