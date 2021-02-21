import telepot
from flask import Flask, render_template, jsonify,request
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep

app = Flask(__name__)

import dynamodb
import jsonconverter as jsonc
global status
status = "off"

my_bot_token = '1693159705:AAE22i1xJIy5mUx3hKiU7a8pRGDvlMwt4mM'
bot = telepot.Bot(my_bot_token)
userid = '210801614'

host = "a3lrhqi4446wbn-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("PubSub-p1804221")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec
my_rpi.connect()



@app.route("/api/getdata",methods=['POST','GET'])
def apidata_getdata():
    if request.method == 'POST' or request.method == 'GET':
        try:
            all_unique = dynamodb.get_all_unique()
            daily_unique_rfid = dynamodb.get_daily_urfid_dynamodb()
            data = {'ambient_data': jsonc.data_to_json(dynamodb.get_data_from_dynamodb()),
                    'human_data': len(daily_unique_rfid)
                    }
            counter = 1
            for i in all_unique:
                emp_data = jsonc.data_to_json(dynamodb.fetch_past_rfid(i))
                #wott = 'emp_data' + str(counter)
                data[i] = emp_data
                #counter = counter + 1
            return jsonify(data)

        except:
            import sys
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

@app.route("/", methods = ['POST', 'GET'])
def home():
    all_unique = dynamodb.get_all_unique()
    return render_template("index.html", value=all_unique)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route("/switch")
def switch():
    global status
    state = request.args.get('state')
    if state=='on':
        ## turn on system functionn 

        message = "on"
        my_rpi.publish("sensors/switch", message, 1)
        ## include changing global variable to on
        status = "on"
        bot.sendMessage(userid, 'Temperature System has been turned: ON')
        return 'system_on'
    elif state =='off':
    	## turn off system function

        message = "off"
        my_rpi.publish("sensors/switch", message, 1)
    	 ## include changing global variable to off
        status = "off"
        bot.sendMessage(userid, 'Temperature System has been turned: OFF')
        return 'system_off'
    ##return ""

@app.route("/system_status")
def system_status():
	global status
	message = status
	return message




app.run(debug=True,host="0.0.0.0",port=8001)
