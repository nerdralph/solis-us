#!/usr/bin/env python
# requires python3, pymodbus, and pyserial
#by Bhuris Mun
# 2023 rewrite by Ralph Doncaster for pymodbus 3.x
# reads from Peacefair PZEM-014 and PZEM-016 power meters
# http://en.peacefair.cn/products/601.html

from pymodbus.client import ModbusSerialClient
from pymodbus.register_read_message import *
import serial.tools.list_ports as lp
import sys, time

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
volt = rsp.registers[0]/10
amp = rsp.registers[1]/1000
power = round(rsp.registers[3]/10 + rsp.registers[4]*6553.6)
energy = rsp.registers[5]/1000
freq = rsp.registers[7]/10
pwfac = rsp.registers[8]/100
alarm = rsp.registers[9]
data={
    "V":volt,
    "A":amp,
    "W":power,
    "kWh":energy,
    "Hz":freq,
    "pfac":pwfac,
    }
print(data)
