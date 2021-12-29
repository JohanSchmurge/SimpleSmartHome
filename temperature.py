import ds18x20
import onewire
from time import sleep_ms
from machine import Pin


OW = onewire.OneWire(Pin(0))
DS = ds18x20.DS18X20(OW)


def get_temp():
    sensors = DS.scan()
    DS.convert_temp()
    sleep_ms(750)
    temp = round(DS.read_temp(sensors[0]), 1)
    return temp
