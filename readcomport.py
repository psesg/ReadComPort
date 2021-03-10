# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
import serial
import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports:
    print ("port='{}'".format(p))
chunk = 1024
#ser1 = serial.Serial('COM1', 9600, timeout=1,   parity=serial.PARITY_NONE)
ser2 = serial.Serial('COM2', 9600, timeout=None,   parity=serial.PARITY_NONE)
#print("connected to: " + ser1.name)
print("connected to: " + ser2.name)
command = b'\x30\x30\x30\x30\x31\x39\x31\x39'
#ser1.write(command)

s = ser2.read(8)

sint = int(s)
print(s)
print("need_read={}".format(sint))
#file = open("leaked.rar", "wb")
n = sint // chunk # chunk
m = sint % chunk # reminder
print(n,m)
# copy /b size.txt+astropy.rar itog.bin
# copy itog.bin com1 /b
#while n > 0:
#    print(n)
#    s = ser2.read(chunk)
#   file.write(s)
#    n = n - 1

#print(sint)
#s = ser2.read(sint)
#ser2.close()
#print(s)
#file.write(s)
#file.close()


