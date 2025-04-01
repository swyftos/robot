from machine import ADC, Pin
from time import sleep
from math import pow

# Constants
GAMMA = 0.7
RL10 = 50  # Resistance of LDR at 10 lux
SERIES_RESISTOR = 5000  # <-- 5kΩ resistor

# LDR on GP26 (ADC0)
ldr = ADC(Pin(26))

def get_lux(analog_value):
    voltage = analog_value / 65535 * 3.3
    try:
        resistance = SERIES_RESISTOR * voltage / (3.3 - voltage)
        lux = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, 1 / GAMMA)
    except ZeroDivisionError:
        lux = 0
    return lux

while True:
    analog_value = ldr.read_u16()
    lux = get_lux(analog_value)

    condition = "Light!" if lux > 50 else "Dark"
    print("Room:", condition, "| Lux: {:.2f}".format(lux))

    sleep(0.5)

