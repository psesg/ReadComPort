# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
import datetime
import serial
import serial.tools.list_ports as port_list
print("Total ports on PC:")
ports = list(port_list.comports())
for p in ports:
    print ("\tport='{}'".format(p))

ser1 = serial.Serial('COM3', 9600, timeout=1,   parity=serial.PARITY_NONE)
ser1.close()
ser2 = serial.Serial('COM4', 115200, timeout=None,   parity=serial.PARITY_NONE, xonxoff=False, rtscts=True,dsrdtr=True)
#print("connected to: " + ser1.name)
print("Will wait connection and data on: " + ser2.name)

need2read = 0
k = 8
inHead = True
while k > 0:
    l = ser2.read(1)
    if inHead:
        #print("Head", k, int(l), type(l))
        if k == 8:
            need2read = need2read + int(l) * 1000 * 1000 * 10
        if k == 7:
            need2read = need2read + int(l) * 1000 * 1000
        if k == 6:
            need2read = need2read + int(l) * 1000 * 100
        if k == 5:
            need2read = need2read + int(l) * 1000 * 10
        if k == 4:
            need2read = need2read + int(l) * 1000
        if k == 3:
            need2read = need2read + int(l) * 100
        if k == 2:
            need2read = need2read + int(l) * 10
        if k == 1:
            need2read = need2read + int(l)
        k = k - 1
        if k == 0 and need2read > 0:
            k = need2read
            print("Get 8 bytes header")
            print("Wait get Body = {}".format(need2read))
            inHead = False
            file = open("leaked.rar", "wb")
            start = datetime.datetime.now()
            ind = 0
    else:
        #print("Body", k, l, type(l))
        file.write(l)
        k = k - 1
        ind = ind + 1
        if ind > 1024 and ind % 1024 == 0:
            print("*",end="")
file.close()
finish = datetime.datetime.now()
elapse = finish - start
#copy itog.bin /b com3 /b
print("\nGot Body {} bytes, file leaked.rar created".format(need2read))
print ("File size: {} elapsed time:  {} s ({} kB/ses)".format(need2read, elapse.total_seconds(),need2read/1024.0/elapse.total_seconds() ))
# 
# mode com3 baud=115200 data=8 parity=n xon=off odsr=on octs=on dtr=on rts=on to=off
# copy itog.bin /b com3 /b
