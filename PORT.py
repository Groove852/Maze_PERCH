#!/usr/bin/env python3
import os
import serial.tools.list_ports_linux as prt

def using_port():
    try:
        prt.comports()
        os.popen(f'sudo -S chmod a+rw {prt.comports()[1][0]}')
        os.system('rosrun rosserial_python serial_node.py _port:={} _baud:=115200'.format(prt.comports()[1][0]))
    except:
        print("Failed!!!")




using_port()
