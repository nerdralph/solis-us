#!/usr/bin/env python
# requires python3, pymodbus 3.x, and pyserial
# 2023 Ralph Doncaster MIT license open source
# reads from Peacefair PZEM-014 and PZEM-016 power meters
# http://en.peacefair.cn/products/601.html

from pymodbus.client import ModbusSerialClient
from pymodbus.register_read_message import *
import serial.tools.list_ports as lp
import math, sys, time

SADDR = 1                               # default slave address
DBG = 0                                 # debug

if len(sys.argv) == 1:
    dev = lp.comports()[0].device
else:
    dev = sys.argv[1]

if DBG: print("using port", dev)
pzem = ModbusSerialClient(port=dev, baudrate=9600) 
pzem.connect()

# read 10 regs starting at address 0
rsp = pzem.read_input_registers(0, count=10, slave=SADDR)
#print(rsp.registers)
sample={
    "volt": rsp.registers[0]/10,
    "amp": rsp.registers[1]/1000 + rsp.registers[2]*65.536, 
    "watt": rsp.registers[3]/10 + rsp.registers[4]*6553.6,
    "Wh": rsp.registers[5] + rsp.registers[6]*65536,
    "freq": rsp.registers[7]/10,
    "pwfac": rsp.registers[8]/100, 
    "alarm": rsp.registers[9],
    }

print(sample)

