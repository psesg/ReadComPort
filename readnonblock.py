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

ser = serial.Serial('COM3', baudrate=921600, timeout=None, bytesize=8, stopbits=serial.STOPBITS_ONE,  parity=serial.PARITY_NONE) #, xonxoff=False, rtscts=True,dsrdtr=True)
print("\n{}: baudrate={} parity={} bytesize={} stopbits={} timeout={}".format(ser.name,ser.baudrate,ser.parity,ser.bytesize,ser.stopbits,ser.timeout))
print("Will wait connection and data on: " + ser.name)

need2read = 0
k = 8
ar_bytes=b''
ar_bytes = ser.read(8)
print(ar_bytes)
need2read = int(ar_bytes.decode("ansi"))
need2readtotal = need2read
print("Get 8 bytes header")
print("Wait get Body file with size = {}".format(need2read))

file = open("zenit_leakednb.rar", "wb")
start = datetime.datetime.now()
while need2read > 0:
    if (ser.inWaiting() > 0):  # if incoming bytes are waiting to be read from the serial input buffer
        data = ser.read(ser.inWaiting())
        readed=len(data)
        need2read = need2read - readed
        progbar(need2read, need2readtotal, 20)
        file.write(data)
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