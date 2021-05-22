# -*- coding: utf-8 -*-
# Step 1: disconnect and reconnect your TTL-to-USB adapter
# Step 2: Type this command in your linux-shell:   dmesg | grep tty
#         You should see which USB-device was connected and how it is called
# Step 3: Edit the name in line 10
import serial
import time
import binascii

serial1 = serial.Serial('/dev/ttyUSB0',115200)  #/dev/ttyUSB0   115200 9600
if serial1.isOpen() :
    print("open success")
else :
    print("open failed")

# Convert hex-value > 10 (which is a..f) to integer-value.
# Probably the original author ot this script did this to gain performance
# against Python's build-in conversion. This workaround is actually working :-/
def cl(a):
    dat1 = a[0:1]

    if dat1 == 'a':
        dat1 = 10
    elif dat1 == 'b':
        dat1 = 11
    elif dat1 == 'c':
        dat1 = 12
    elif dat1 == 'd':
        dat1 = 13
    elif dat1 == 'e':
        dat1 = 14
    elif dat1 == 'f':
        dat1 = 15
        
    return dat1

def main():
    global serial1
    time.sleep(0.2) 
    num=serial1.inWaiting()
            
    if num: 
        try:   #try to read hexadecimal data
            interface_data = serial1.read(num)
            # distance reading will look like this: \x01\x03\x02\x08\xdb\xff\xdf
            #print(interface_data)   

            data= str(binascii.b2a_hex(interface_data))
            # distance reading converted will look like this:01030208dbffdf
            #print(data)   
            # 01030208dbffdf: 010302=header, 08db=distance in hex, the rest I don't care about
            # For more info see TOF400F datasheet.

            if(len(data)>8):
                byte1_low = data[9:10]
                byte2_high = data[10:11]
                byte2_low = data[11:12]
                
                # High-part of first byte not included in calculation, as 0x0fff is already 4095mm, which
                # is more than max range of TOF400F sensor.
                distance_value = 0.0 # needs to be float from beginning, otherwise runtime-conversion will take too long
                distance_value = int(cl(byte2_low)) + int(cl(byte2_high))*16 + int(cl(byte1_low))*256
                print("distance:", distance_value, "mm")

        except:
            pass

while True:
    main()
