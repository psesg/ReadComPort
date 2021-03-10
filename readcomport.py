# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports
import serial
ser = serial.Serial('COM1', 19200, timeout=1,   parity=serial.PARITY_NONE)

print("connected to: " + ser.portstr)
# copy /b size.txt+astropy.rar itog.bin