import network
import time
from config import SSID, AP_SSID, AP, STA
from machine import Pin

network.WLAN(network.AP_IF).active(AP)
wlan = network.WLAN(network.STA_IF)
wlan.active(STA)
ap = network.WLAN(network.AP_IF)
ap.config(essid=AP_SSID[0], password=AP_SSID[1], channel=11, authmode=3)
ap.active(AP)
WLAN_LED = Pin(14, Pin.OUT)


def start():
    WLAN_LED.off()
    if wlan.isconnected():
        print('Wi-Fi already connected.')
    else:
        t0 = time.time()+20
        wlan.connect(SSID[0], SSID[1])
        while not wlan.isconnected():
            time.sleep_ms(500)
            if t0 < time.time():
                print('Wi-fi connection timeout')
                break
    WLAN_LED.on()
    print(wlan.ifconfig())


def stop():
    wlan.disconnect()


def status(t):
    if wlan.isconnected():
        return True
    else:
        WLAN_LED.off()
        # debug('Wlan disconnected.')
        return False
