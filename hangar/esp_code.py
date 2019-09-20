# Firmware http://micropython.org/download#esp32

# https://www.arduinoecia.com.br/2019/04/programe-o-esp32-em-python-micropython.html

# https://www.fernandok.com/2018/10/introducao-programacao-do-esp32.html

# Tito https://docs.google.com/document/d/1Ia1TMb3OrdjhLJ0lI0MpyokDFV1MPvqIwSMHfouypyA/edit?ts=5d2debaf

# Documentacao da micropython
# https://docs.micropython.org/en/latest/esp32/quickref.html#networking
import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points
wlan.isconnected()      # check if the station is connected to an AP
wlan.connect('essid', 'password') # connect to an AP
wlan.config('mac')      # get the interface's MAC adddress
wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.config(essid='ESP-AP') # set the ESSID of the access point
ap.active(True)         # activate the interface

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('essid', 'password')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
