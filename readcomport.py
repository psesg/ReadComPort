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

ser = serial.Serial('COM3', baudrate=115200, timeout=None, bytesize=8, stopbits=serial.STOPBITS_ONE,  parity=serial.PARITY_NONE) #, xonxoff=False, rtscts=True,dsrdtr=True)
print("\n{}: baudrate={} parity={} bytesize={} stopbits={} timeout={}".format(ser.name,ser.baudrate,ser.parity,ser.bytesize,ser.stopbits,ser.timeout))
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
            print(ar_bytes)
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
ser.close()
finish = datetime.datetime.now()
elapse = finish - start

print("\nGot Body {} bytes, file leaked.rar created".format(need2read))
print ("File size: {} elapsed time:  {} s ({} kB/ses)".format(need2read, elapse.total_seconds(),need2read/1024.0/elapse.total_seconds() ))

# usb-rs-232-NullModemCable-rs-232-usb:
# copy size.txt+astropy.rar /b itog.bin /b
#
#     mode com3 baud=115200 parity=n data=8
#     Скорость:              115200
#     Четность:              None
#     Биты данных:           8
#     Стоповые биты:         1
#     Таймаут:               OFF
#     XON/XOFF:              OFF
#     Синхронизация CTS:     OFF
#     Синхронизация DSR:     OFF
#     Чувствительность DSR:  OFF
#     Цепь DTR:              ON
#     Цепь RTS:              ON
#
# copy itog.bin /b com3 /b
#
#Got Body 18349 bytes, file leaked.rar created
#File size: 18349 elapsed time:  1.598731 s (11.208230348007264 kB/ses)