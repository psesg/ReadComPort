# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
import datetime
import serial
import serial.tools.list_ports as port_list

print("Total ports on PC:")
ports = list(port_list.comports())

if len(ports) < 1:
    print("serial ports not found!")
    exit(-10)
else:
    for p in ports:
        print ("\tport='{}'".format(p))

def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')

ser = serial.Serial('COM5', baudrate=19200, timeout=None, bytesize=8, stopbits=serial.STOPBITS_ONE,  parity=serial.PARITY_NONE) #, xonxoff=False,  rtscts=True,dsrdtr=True)
print("\n{}: baudrate={} parity={} bytesize={} stopbits={} timeout={}".format(ser.name,ser.baudrate,ser.parity,ser.bytesize,ser.stopbits,ser.timeout))
print("Will wait connection and data on: " + ser.name)
ser.flushInput()


need2read = 8
headON = True
head=b''
k=0
while need2read > 0:
    if (ser.inWaiting() > 0):  # if incoming bytes are waiting to be read from the serial input buffer
        data = ser.read(ser.inWaiting())
        readed=len(data)
        #print(readed,data.hex())
        if headON:
            head = head + data
            if len(head) > 8:
                need2readtotal = int(head[:8].decode("ansi"))
                print("Get 8 bytes header, wait get Body file with size = {}".format(need2readtotal))
                file = open("zenit_leakednb.rar", "wb")
                start = datetime.datetime.now()
                file.write(head[8:])
                k =  len(head[8:])
                #print(k)
                headON = False
                need2read = need2readtotal  - len(head[8:])
                #print("need2read = {} = {} - {}".format(need2read, need2readtotal,len(head[8:] )))
        else:
            file.write(data)
            k =  len(data)
            #print("file.write else {}".format(len(data)))
            need2read = need2read - len(data)
            #print(k)
            progbar(need2read, need2readtotal, 40)

file.close()
ser.close()
finish = datetime.datetime.now()
elapse = finish - start
print("\nGot Body {} bytes, file zenit_leakednb.rar created".format(need2readtotal))
print ("File size: {} elapsed time:  {} s ({} kB/ses)".format(need2readtotal, elapse.total_seconds(),need2readtotal/1024.0/elapse.total_seconds() ))
# File size: 2750128 elapsed time:  31.498 s (85.26483824369801 kB/ses)
# baudrate=921600
# mode com6 baud=921600 parity=n data=8
#     Скорость:              921600
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