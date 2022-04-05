import time
import board
import busio
import analogio

API_KEY = "U5XA7UEOCYYLE12W"  # ThingsSpeak channel API
SSID = "MySpectrumWiFi88-2G" #wifi setup
PASSWORD = "livelypoodle574"  

uart = busio.UART(board.TX, board.RX, baudrate=115200, bits=8,
                  parity=None, stop=1, timeout=1)

analogsensorpin = board.A1  # Change this to your specific pin
analogsensor = analogio.AnalogIn(analogsensorpin)

analogsensorpin2 = board.A2  # Change this to your specific pin
analogsensor2 = analogio.AnalogIn(analogsensorpin2)


print("Resetting the ESP01")
uart.write(b'AT+RST\r\n')
time.sleep(5)
uart.write(b'AT+CWMODE=1\r\n')
time.sleep(5)
uart.write(b'AT+CWJAP="'+bytearray(str(SSID))+b'","'+bytearray(str(PASSWORD))+b'"\r\n')
time.sleep(5)

while True:
    data = uart.read(32)

    if data is not None:
        data_string = ''.join([chr(b) for b in data])
        print(data_string,end="")
        time.sleep(1)

    Vout = analogsensor.value / 65535 #Volts
    Vsec = analogsensor2.value / 65535

    Cout = (Vout-Vsec)/(3300)
    Pout = Cout*Vout
    watts = Pout*1000 #mW
    print("Sensor Value = "+str(watts)+" mW")
    time.sleep(1)

    uart.write(b"AT+CIPMODE=0\r\n")
    time.sleep(3)
    uart.write(b'AT+CIPSTART="TCP","api.thingspeak.com",80\r\n')
    time.sleep(5)
    length = len('GET /update?api_key='+API_KEY+'&field1='+str(watts)+
                 ' HTTP/1.1')+29

    uart.write(b'AT+CIPSEND=' + bytearray(str(length)) + b'\r\n')
    time.sleep(2)

    uart.write(b'GET /update?api_key='+bytearray(API_KEY)+b'&field1='+
               bytearray(str(watts))+
               b' HTTP/1.1\r\n')
    time.sleep(10)
    uart.write(b'Host:api.thingspeak.com\r\n\r\n')
    time.sleep(10)
    uart.write(b'AT+CIPCLOSE\r\n')
    time.sleep(20)
