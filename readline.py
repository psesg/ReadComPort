# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
import datetime
import serial
import serial.tools.list_ports as port_list

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s
        #self.cont = True

    def readline(self):
        #end = self.buf.find(b"zzz")
        #if end >= 0:
        #    self.cont = False
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return(r)
        while True:
            i = max(1, min(1024, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return (r)
            else:
                self.buf.extend(data)

print("Total ports on PC:")
ports = list(port_list.comports())

if len(ports) < 1:
    print("serial ports not found!")
    exit(-10)
else:
    for p in ports:
        print ("\tport='{}'".format(p))

ser = serial.Serial('COM4', baudrate=115200, timeout=None, bytesize=8, stopbits=serial.STOPBITS_ONE,  parity=serial.PARITY_NONE, xonxoff=True) #, xonxoff=False,  rtscts=True,dsrdtr=True)
print("\n{}: baudrate={} parity={} bytesize={} stopbits={} timeout={} xon={}".format(ser.name,ser.baudrate,ser.parity,ser.bytesize,ser.stopbits,ser.timeout, ser.xonxoff))
print("Will wait connection and data on: " + ser.name)
#ser.flushInput()
print("---------------begin data----------------")
rl = ReadLine(ser)
contread = True
while contread:
    bytes = rl.readline()
    #print(bytes)
    if bytes == b'zzz\r\n':
        break
    #contread = end
    stri = bytes.decode("utf-8")
    print(stri,end="")
print("---------------end data----------------")

# mode com5 baud=115200 parity=n data=8 xon=on
# copy LICENSE_UTF8.txt com4
# copy LICENSE_ANSI.txt  com4