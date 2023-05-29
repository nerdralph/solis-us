#!/usr/bin/env python3
#by Bhuris Mun
# 2023 updates by Ralph Doncaster for pymodbus 3.x
# reads from Peacefair PZEM-014 and PZEM-016 power meters
# http://en.peacefair.cn/products/601.html

from pymodbus.client import ModbusSerialClient
import time, json, math
from pymodbus.register_read_message import *

#client = ModbusSerialClient(framer='rtu', port='/dev/ttyUSB0', timeout=0.3, baudrate=9600) 
client = ModbusSerialClient(port='/dev/ttyUSB0', timeout=1, baudrate=9600) 
client.connect()
#print(client.connect())

def main():
    value = client.read_input_registers(0, 10, unit=0x01) #read from unit 0x01
    print(value)
    #print(value.registers) #for prove test
    volt = value.registers[0]*0.1
    amp = value.registers[1]*0.001
    power = value.registers[3]*0.1
    energy = value.registers[5]*0.001
    freq = value.registers[7]*0.1
    pwfac = value.registers[8]*0.01
    alarm = value.registers[9]
    if alarm == 0x0000:
        alarmtran = 'NORMAL JA'
    elif alarm == 0xFFFF:
        alarmtran = 'ALARM'
    else:
        alarmtran = 'N/A'
    pwangle=math.acos(pwfac)
    apparent = power/math.cos(pwangle)
    reactive = apparent*math.sin(pwangle)
    impedance= apparent/(amp*amp)
    rinline = impedance*math.cos(pwangle)
    xinline = impedance*math.sin(pwangle)
    data={}
    data={
        "volt":volt,
        "amp":amp,
        "realpower":power,
        "energy":energy,
        "freq":freq,
        "pwfac":pwfac,
        "reactive":reactive,
        "apparent":apparent,
        "powerangle":pwangle,
        "impedance":impedance,
        "rinline":rinline,
        "xinline":xinline,
        "status":alarmtran
        }
    dataff=json.dumps(data) # format data to json
    print(dataff) # for stdout nodered

main()
