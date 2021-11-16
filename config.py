#    This program is free software: you can redistribute it and/or modify     
#    it under the terms of the GNU General Public License as published by     
#    the Free Software Foundation, either version 3 of the License, or        
#    (at your option) any later version.                                      
#                                                                             
#    This program is distributed is AS IS, WITHOUT ANY WARRANTY;                        
#                                                                             
#    You should have received a copy of the GNU General Public License        
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    
#                                                                             
#    Copyright by dr.Schmurge (dr.schmurge@dismail.de)

SSID = ('WiFi', 'fd57a224')
#SSID = ('js', ':g_JhL-XPvo92dqaZ', b'\xc0\xf8\xda\x9b\x88\x08')              # SSID, password for Wi-Fi station interface
AP_SSID = ('MP', 'M1cr0Pyth0n')                 # Default SSID and password for AP interface
AP = True                                       # Access Point interface
STA = True                                      # Station interface

LOG = True                                     # Enable logging
#if LOG:
    #LOG_LEVEL = 'ERROR'                         # Loglevel can be ERROR, DEBUG, INFO
    #LOG_DIR = 'log'
    #LOG_FILE = LOG_DIR + '/%d-%d-%d.log'
    #LOG_AGE = 1                                 # Logfiles older than LOG_AGE will be remove. Remember, that flash size is 4MiB!
    #SYSLOG_SERVER = '0.0.0.0' 

#CHECK_UPDATES = False
#if CHECK_UPDATES:
    #AUTO_UPDATE = False
    #AUTOUPDATE_URL = 'http://example.com'

TZ = 3                                          # Time zone

#LOCALE = 'ru'
