import busio             #module setup
import time
import board
import adafruit_am2320
from analogio import AnalogIn

uart = busio.UART(board.TX, board.RX, baudrate=115200) #uart setup
i2c = busio.I2C(board.SCL, board.SDA)       #humidity sensor-i2c protocol
am = adafruit_am2320.AM2320(i2c)

temperature = 0           #parameters
Vout = 0                  #LM35 voltage drop
Vout2 = 0                 #Photocell voltage drop

analog_in = AnalogIn(board.A0)              #pins setup
analog_in2 = AnalogIn(board.A1)


def get_value(pin):               #voltage values setup for each pin
    return (pin.value) 

def find():              #read uart feedback function
    if data is not None:
        data_string = ''.join([chr(b) for b in data])
        print(data_string, end="")
        time.sleep(3)
    return

while True:
    Vout = (int(get_value(analog_in)) * 5 / 65536)   #Vdrop from LM35
    Vout2 = ((int(get_value(analog_in2)) * 3300) / 65536) #photocell Vdrop
    temperature = 9 * (Vout / .01) / 5 + 32  #Convert LM35 Vdrop to Fahren
    data = uart.readline() #uart read all data feedback

    uart.write('AT+RST\r\n')                #HTTP Commands
    find()

    uart.write('AT+CWMODE=1\r\n')
    find()

    uart.write('AT+CWJAP="bucknell_iot",""\r\n')
    find()

    uart.write('AT+CIPMODE=0\r\n')
    find()

    uart.write('AT+CIPSTART="TCP","api.thingspeak.com",80\r\n')
    find()

    uart.write('AT+CIPSEND=150\r\n')
    find()

    uart.write("GET /update?api_key=WESYI6EBFKIZP22L&field2="+str(Vout2)+"&field3="+str(temperature)+"&field4="+str(am.relative_humidity)+"\r\n")
    find()

    uart.write('AT+CIPCLOSE\r\n')
    find()
