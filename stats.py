#!/usr/bin/env python3

# solis 1P-XK-4G-US inverter status

from datetime import datetime
import os
from pysolarmanv5 import PySolarmanV5, V5FrameError
import sys
import time
import umodbus.exceptions

PVIP = os.getenv("PVIP")
PVSN = int(os.getenv("PVSN"))
MINPOWER = 30

def stats():
    ts = datetime.now().isoformat(timespec="seconds")
    print(f"{ts},", end='')
    try:
        modbus = PySolarmanV5(
            PVIP, PVSN, port=8899, mb_slave_id=1, verbose=False
        )
        # offset address by -1 for function 4
        power = modbus.read_input_registers(register_addr=3005, quantity=3)
        wac = power[0]
        wdc = power[2]
        if wac < MINPOWER:
            raise Exception()
        eff = wac/wdc * 100
        print(f"{wac},{wdc},{eff:.1f}%")
    except Exception: 
        print("0,0,0%")
    
    sys.stdout.flush()
    return

if __name__ == "__main__":
    print("Time, W AC, W DC, efficiency")
    while 1:
        stats()
        # repeat every 3m, allowing for 1s execution time
        time.sleep(299)

