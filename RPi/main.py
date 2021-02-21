import RPi.GPIO as GPIO
import signal
import serial
from threading import Thread
from time import sleep
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from rpi_lcd import LCD



def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	if message.payload == "off":
		#switchOff
		lcd.text('Temp System is', 1)
		lcd.text('OFFLINE', 2)
		ser.write("SYSTEMOFF".encode())
		print("off")
		
	if message.payload == "on":
		#switchOn
		lcd.text('Temp System is', 1)
		lcd.text('ONLINE', 2)
		ser.write("SYSTEMON".encode())
		print("on")
		
		
		
listening = True
uid = None 
prev_uid = None
continue_reading = True
ambienttemp = 0.0
temperature = 0.0
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()
tapRFID = False
host = "a3lrhqi4446wbn-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"
lcd = LCD()

my_rpi = AWSIoTMQTTClient("PubSub1-p1804221")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

my_rpi.connect()
my_rpi.subscribe("sensors/switch", 1, customCallback)


        

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    
def listToString(s):  
    # initialize an empty string 
    str1 = ""  
    # traverse in the string   
    for ele in s:  
        str1 += str(ele)   
    # return string   
    return str1  
    
def activate_LCD():
   print('Displaying temperature on LCD')
   global lcd
   global temperature
   lcd.text('Detected Temp:', 1)
   lcd.text('{:.1f}*C'.format(temperature), 2)
   sleep(7)
   lcd.clear()
        
    
# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe("sensors/temp", 1, customCallback)
sleep(2)

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)



# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips.
# If one is near it will get the UID


def read_card_main():
	global temperature
	global listening
	
	while continue_reading:
	    import mfrc522
	    # Create an object of the class MFRC522
	    mfrc522 = mfrc522.MFRC522()
	    # Scan for cards    
	    (status,TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)
	    
	    # Get ambient temperature all the time
	    if status == 2:
			if ser.in_waiting > 0:
				received_serial = ser.readline().decode().strip()
				temperature = round(float(received_serial),1)
				print('ambient: '+ str(temperature))
				message = {}
				message["deviceid"] = "tempsensor1"
				import datetime as datetime
				now = datetime.datetime.now()
				message["date_time"] = now.isoformat()      
				message["ambient_temp"] = temperature
				import json
				my_rpi.publish("sensors/ambient", json.dumps(message), 1)
	
	    # If a card is found
	    if status == 0:
	        # Get the UID of the card
	        (status,uid) = mfrc522.MFRC522_Anticoll()

	        if uid:
	                lcd.text("Please move", 1)
	                lcd.text("closer", 2)
	                ser.reset_input_buffer()
	                tapRFID = True
	                print("New card detected! UID of card is {}".format(uid))
	                ser.write("READY".encode())
	                while tapRFID:
	                        if ser.in_waiting > 0:
	                                received_serial = ser.readline().decode().strip()
	                                temperature = round(float(received_serial),1)
	                                print(temperature)
	                                tapRFID = False
	                message = {}
	                message["deviceid"] = 'empstore'
	                message["rfid"] = listToString(uid)
	                import datetime as datetime
	                now = datetime.datetime.now()
	                message["date_time"] = now.isoformat()  
	                message["temperature"] = temperature

	                import json
	                my_rpi.publish("sensors/temp", json.dumps(message), 1)
	                activate_LCD()
	                
def read_ambient():
	print('reading ambient')
	global listening
	while listening:
		if ser.in_waiting > 0:
			received_serial = ser.readline().decode().strip()
			print(received_serial)
			
if __name__ == '__main__':
	read_card_main()
	
           

