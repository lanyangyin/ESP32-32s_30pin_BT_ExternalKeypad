# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import network
wlan = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)
wlan.active()
ap.active()
wlan.active(False)
ap.active(False)
