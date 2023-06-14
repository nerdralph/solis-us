#!/usr/bin/env python3

# solis 1P-XK-4G-US inverter status

from datetime import datetime
import os
from pysolarmanv5 import PySolarmanV5, V5FrameError
import sys
import time
import umodbus.exceptions

# Solis MODBUS registers fn code 0x04
# 3005 = U32 active power(AC) 1W
#   06 = U16 active power LSB16
# 3007 = U32 DC power 1W
#   08 = U16 DC power LSB16
# 3015 = U16 energy today 0.1kWh
# 3036 = U16 phase C voltage 0.1V
# 3039 = U16 phase C current 0.1A
# 3042 = U16 inverter temperature 0.1C

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
        # subtract 6 from address for out[] index
        out = modbus.read_input_registers(register_addr=3005, quantity=37)
        wac = out[0]
        wdc = out[2]
        if wdc == 0:
            raise Exception()
        eff = wac/wdc * 100
        c = out[36]/10
        kWh = out[9]/10
        V = out[30]/10
        A = out[33]/10
        print(f"{wac},{wdc},{eff:.1f}%,{c},{kWh},{V},{A}")
    except Exception: 
        print("read failed")

    sys.stdout.flush()
    return

if __name__ == "__main__":
    print("Time, W AC, W DC, efficiency, oC, kWh, Volts, Amps")
    while 1:
        stats()
        # repeat every 3m, allowing for 2s fetch time
        time.sleep(298)

