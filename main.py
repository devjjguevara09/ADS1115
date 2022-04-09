"""
Elaborado por: Juan J. Guevara - devjjguevara09@outlook.com
Última revisión: 17-03-2022
Observaciones: Funcionamiento comprobado con board ADS1115 clon de versión de Adafruit + ESP8266 NodeMCU

Este script está basado en la librería y documentación disponible en: https://micropython-ads1015.readthedocs.io/en/latest/index.html

Premisas:
1. El módulo ADS1115 posee cuatro canales de conversón (An0..An3), se pueden utilizar como canales independientes, pero la lectura es
mas estable si se utiliza una lectura diferencial en la cual el resultado de la conversión es la diferencia de voltaje entre dos canales.
En este ejemplo se establecen los pares de canales diferenciales An0-An1 en donde An0 = Vin1 y An1 = GND. De igual manera se utiliza el
par diferencial An2-An3, siendo An2 = vin2 y An3 = GND.

2. La ganancia define el rango de las lecturas de voltaje de entrada, de acuerdo con la siguiente tabla:
    Valor	Ganancia	Voltaje
    0	    ⅔×	        6.144V
    1	    1×	        4.096V
    2	    2×	        2.048V
    3	    4×	        1.024V
    4	    8×	        0.512V
    5	    16×	        0.256V

El valor de la ganancia debe establecerse en función del voltaje Vin máximo que se espera recibir el cual nunca debe exceder +0.3V respecto
a VDD.

Si la ganancia es 1x = 4.096V, entonces cada bit equivale a: 4.096V / (2^15 - 1) = 0.000125V = 0.125mV 

Si Vin = 2.5V entonces 2.5/0.000125 = 20000

"""


from machine import Pin, I2C
from time import sleep_ms
import ads1x15

#Constante para el cáclulo de la distancia
const_d = 30.7625

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

i2c.scan()  #Si ya se conoce la dirección del dispositivo esta instrucción no es necesaria

adc = ads1x15.ADS1115(i2c, 0x48)

adc.gain = 1

def leerValor(canal1, canal2):
    lectura = adc.diff(canal1, canal2)
    return lectura

def calcularVoltaje(canal, lectura):
    voltaje = float(lectura * 0.000125)
    distancia = float((lectura / const_d) + 205)
    print("AN", canal, "=", lectura, ", Voltaje =", "%.3f" %voltaje, "V", "Distancia(mm):", "%.3f" %distancia)

while True:
    valor = leerValor(0, 1)
    calcularVoltaje(0, valor)
    sleep_ms(1000)
#    valor = leerValor(2, 3)
#    calcularVoltaje(2, valor)
#    sleep_ms(1000)