#!/usr/bin/env python
# 2023 Ralph Doncaster
# reads from Peacefair PZEM-014 and PZEM-016 power meters
# http://en.peacefair.cn/products/601.html
# post data to PVOutput API pvoutput.org/help/api_specification.html
# requires pymodbus 3.x
# one optional argument for serial port

from pymodbus.client import ModbusSerialClient
from pymodbus.register_read_message import *
import serial.tools.list_ports as lp
from datetime import datetime
import math, sys, time

SADDR = 1                               # default slave address
DBG = 0                                 # debug

if len(sys.argv) == 1:
    # use first serial port found
    dev = lp.comports()[0].device
else:
    dev = sys.argv[1]

if DBG: print("using port", dev)
pzem = ModbusSerialClient(port=dev, baudrate=9600) 
pzem.connect()

# read 10 regs starting at address 0
rsp = pzem.read_input_registers(0, count=10, slave=SADDR)
#print(rsp.registers)
volt = rsp.registers[0]/10
amp = rsp.registers[1]/1000
power = round(rsp.registers[3]/10 + rsp.registers[4]*6553.6)
energy = rsp.registers[5]
now = datetime.now()
date = now.strftime("%Y%m%d") 
hm = now.strftime("%H%M")
data={
    "d":date,
    "t":hm,
    "v1":energy,
    "v2":power,
    "v6":volt,
    "v5":amp,
    }
print(data)
