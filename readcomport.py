# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
import serial
import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports:
    print ("port='{}'".format(p))

ser1 = serial.Serial('COM3', 9600, timeout=1,   parity=serial.PARITY_NONE)
ser1.close()
ser2 = serial.Serial('COM4', 9600, timeout=None,   parity=serial.PARITY_NONE)
#print("connected to: " + ser1.name)
print("connected to: " + ser2.name)

need2read = 0
k = 8
inHead = True
while k > 0:
    l = ser2.read(1)
    if inHead:
        print("Head", k, int(l), type(l))
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
            print("Wait get Body = {}".format(need2read))
            inHead = False
            file = open("leaked.rar", "wb")
    else:
        #print("Body", k, l, type(l))
        file.write(l)
        k = k - 1
file.close()
#copy itog.bin /b com3 /b
print("leaked.rar - created")


