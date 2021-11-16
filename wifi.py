#    This program is free software: you can redistribute it and/or modify     
#    it under the terms of the GNU General Public License as published by     
#    the Free Software Foundation, either version 3 of the License, or        
#    (at your option) any later version.                                      
#                                                                             
#    This program is distributed is AS IS, WITHOUT ANY WARRANTY.                        
#                                                                             
#    You should have received a copy of the GNU General Public License        
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    
#                                                                             
#    Copyright by dr.Schmurge (dr.schmurge@dismail.de) 

import network, time
from config import SSID, AP, STA
from machine import Pin

network.WLAN(network.AP_IF).active(AP)
wlan = network.WLAN(network.STA_IF)
wlan.active(STA)

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

def status():
    if wlan.isconnected(): return True
    else:
        WLAN_LED.off()
        debug('Wlan disconnected.')
        return False



                
                    
            



