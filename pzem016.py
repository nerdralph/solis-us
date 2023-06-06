#!/usr/bin/env python3
#by Bhuris Mun
# 2023 rewrite by Ralph Doncaster for pymodbus 3.x
# reads from Peacefair PZEM-014 and PZEM-016 power meters
# http://en.peacefair.cn/products/601.html

from pymodbus.client import ModbusSerialClient
from pymodbus.register_read_message import *
import serial.tools.list_ports as lp
import json, math, sys, time

SADDR = 1                               # default slave address

if len(sys.argv) == 1:
    dev = lp.comports()[0].device
else:
    dev = sys.argv[1]

print("using port", dev)
pzem = ModbusSerialClient(port=dev, baudrate=9600) 
pzem.connect()

# read 10 regs starting at address 0
rsp = pzem.read_input_registers(0, count=10, slave=SADDR)
#print(rsp.registers)
volt = rsp.registers[0]/10
amp = rsp.registers[1]*0.001
power = rsp.registers[3]/10 + rsp.registers[4]*6553.6
energy = rsp.registers[5]*0.001
freq = rsp.registers[7]/10
pwfac = rsp.registers[8]*0.01
alarm = rsp.registers[9]
data={
    "volt":volt,
    "amp":amp,
    "power(W)":power,
    "energy(kWh)":energy,
    "freq":freq,
    "pwfac":pwfac,
    "status":alarm
    }
dataff=json.dumps(data)             # format data to json
print(dataff)
