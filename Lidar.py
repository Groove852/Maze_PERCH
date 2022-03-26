#!/usr/bin/env python3
import os
import serial.tools.list_ports_linux as prt

def using_port():
    try:
        prt.comports()
        os.popen(f'sudo chmod a+rw {prt.comports()[0][0]}')
        os.system(f'roslaunch hls_lfcd_lds_driver hlds_laser.launch')
    except:
        print("Failed!!!")




using_port()
