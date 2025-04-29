from machine import Pin, PWM, ADC
from time import sleep_ms

# --- Classe Motor ---
class Motor:
    def __init__(self, pwm_pin, cw_pin, acw_pin, freq=50):
        self.pwm = PWM(Pin(pwm_pin))
        self.pwm.freq(freq)
        self.cw = Pin(cw_pin, Pin.OUT)
        self.acw = Pin(acw_pin, Pin.OUT)

    def set_speed(self, speed_pct):
        speed = max(0, min(speed_pct, 100))
        self.pwm.duty_u16(int(speed / 100 * 65535))

    def forward(self, speed_pct):
        self.cw.value(1)
        self.acw.value(0)
        self.set_speed(speed_pct)

    def backward(self, speed_pct):
        self.cw.value(0)
        self.acw.value(1)
        self.set_speed(speed_pct)

    def stop(self):
        self.cw.value(0)
        self.acw.value(0)
        self.set_speed(0)

# --- Brochage et objets moteurs ---
mot1 = Motor(pwm_pin=5, cw_pin=8, acw_pin=9)
mot2 = Motor(pwm_pin=27, cw_pin=19, acw_pin=18)

# --- Capteurs LDR ---
ldr_avant   = ADC(0)   # GP26
ldr_arriere = ADC(2)   # GP28

# --- Paramètres ---
ALPHA = 0.2    # lissage exponentiel
HYST  = 2000   # hystérésis

# --- Calibration LDR ---
def calibrate(adc, samples=50):
    vals = [adc.read_u16() for _ in range(samples)]
    return min(vals), max(vals)

# --- Boucle principale ---
def comportement_lumiere():
    print("--- Calibration des LDR ---")
    min_a, max_a = calibrate(ldr_avant)
    min_r, max_r = calibrate(ldr_arriere)
    seuil = ((min_a + max_a) + (min_r + max_r)) // 4
    print("Seuil calculé :", seuil)

    prev_avant   = None
    prev_arriere = None

    while True:
        # Lecture brute
        raw_a = ldr_avant.read_u16()
        raw_r = ldr_arriere.read_u16()

        # Lissage exponentiel
        if prev_avant is None:
            prev_avant, prev_arriere = raw_a, raw_r
        else:
            prev_avant   = int(ALPHA * raw_a + (1 - ALPHA) * prev_avant)
            prev_arriere = int(ALPHA * raw_r + (1 - ALPHA) * prev_arriere)

        a, r = prev_avant, prev_arriere
        print("Avant:", a, "| Arrière:", r)

        # Décision : avancer / reculer selon intensité lumineuse
        if a > seuil + HYST and a > r:
            print("→ Lumière devant : j'avance")
            mot1.forward(70)
            mot2.forward(70)

        elif r > seuil + HYST and r > a:
            print("→ Lumière derrière : je recule")
            mot1.backward(70)
            mot2.backward(70)

        # Valeurs proches → avance ou recule selon capteur le plus exposé
        elif abs(a - r) < HYST:
            if a > r:
                print("→ Intensité légèrement plus élevée devant : j'avance")
                mot1.forward(50)
                mot2.forward(50)
            else:
                print("→ Intensité légèrement plus élevée derrière : je recule")
                mot1.backward(50)
                mot2.backward(50)

        else:
            # Pas de lumière claire
            print("→ Pas de lumière claire : je m'arrête")
            mot1.stop()
            mot2.stop()

        sleep_ms(300)

# --- Point d'entrée et gestion d'interruption ---
def main():
    try:
        comportement_lumiere()
    except KeyboardInterrupt:
        mot1.stop()
        mot2.stop()
        print("Arrêt du programme")

if __name__ == '__main__':
    main()
