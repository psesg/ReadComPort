# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
import serial
import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports:
    print ("port='{}'".format(p))

ser = serial.Serial('COM3', 9600, timeout=1,   parity=serial.PARITY_NONE)

print("connected to: " + ser.portstr)
command = b'\x30\x30\x30\x30\x31\x39\x31\x39'
ser.write(command)
s = ser.read(8)
print(s)
print("read={}".format(s))
# copy /b size.txt+astropy.rar itog.bin


