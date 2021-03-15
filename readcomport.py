# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
import datetime
import serial
import serial.tools.list_ports as port_list
chunk = 1024
print("Total ports on PC:")
ports = list(port_list.comports())

if len(ports) < 1:
    print("serial ports not found!")
    exit(-10)
else:
    for p in ports:
        print ("\tport='{}'".format(p))

ser = serial.Serial('COM4', 19200, timeout=None,   parity=serial.PARITY_NONE) #, xonxoff=False, rtscts=True,dsrdtr=True)
print("Will wait connection and data on: " + ser.name)

need2read = 0
k = 8
ar_bytes=b''
inHead = True
while k > 0:
    l = ser.read(1)
    ar_bytes = ar_bytes + l
    if inHead:
        #print("Head", k, int(l), type(l))
        k = k - 1
        if k == 0:
            need2read = int(ar_bytes.decode("ansi"))
            #print(need2read)
        if k == 0 and need2read > 0:
            k = need2read
            print("Get 8 bytes header")
            print("Wait get Body file with size = {}".format(need2read))
            print("One asterisk = {} bytes".format(chunk))
            inHead = False
            file = open("zenit_leaked.rar", "wb")
            start = datetime.datetime.now()
            ind = 0
            brl = 0
    else:
        #print("Body", k, l, type(l))
        file.write(l)
        k = k - 1
        ind = ind + 1
        if ind > chunk and ind % chunk == 0:
            brl = brl + 1
            if brl > 65:
                print("*")
                brl = 0
            else:
                print("*",end="")
file.close()
finish = datetime.datetime.now()
elapse = finish - start

print("\nGot Body {} bytes, file leaked.rar created".format(need2read))
print ("File size: {} elapsed time:  {} s ({} kB/ses)".format(need2read, elapse.total_seconds(),need2read/1024.0/elapse.total_seconds() ))
# copy size.txt+astropy.rar /b itog.bin /b
# mode com3 baud=115200 data=8 parity=n xon=off odsr=on octs=on dtr=on rts=on to=off
# mode com3 baud=19200 parity=n data=8 stop=1 to=off xon=off odsr=off octs=off dtr=on rts=on idsr=off
# copy itog.bin /b com3 /b
