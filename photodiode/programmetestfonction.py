from machine import ADC
import time

adc = ADC(26)  # Correct way to create an ADC object from GPIO 26

while True:
    digital_value = adc.read_u16()
    print("ADC value =", digital_value)
    volt = 3.3 * (digital_value / 65535)
    print("Voltage: {:.2f} V".format(volt))
    time.sleep(1)

