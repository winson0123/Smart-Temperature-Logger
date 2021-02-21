# Smart-Temperature-Loggger
## Table of Contents
* Section 1 - Overview
* Section 2 - Hardware Requirements
* Section 3 - Hardware Setup
* Section 4 - Software Setup
* Section 5 - AWS/Create a “Thing”
* Section 6 - AWS/DynamoDB Setup
* Section 7 - AWS/Simple Notification System
* Section 8 - AWS/EC2 Hosting of Web Application
* Section 9 - Raspberry Pi Configuration
* Section 10 - Raspberry Pi Setup
* Section 11 - Arduino Setup
* Section 12 - Expected Outcome

## Section 1 - Overview
### Project Description:
It is a Smart Temperature Logger. The application involves an infrared temperature sensor which measure the valid users’ temperature, who have scanned their RFID access card. The temperature measured will then be stored into a database which will be monitored and an alert will be sent whenever the temperature exceeds a certain value. The target audiences are for corporations or institutions that would like to manage who is able to enter based on their current temperature.
### How the final RPI set-up looks like:
![Picture1](https://user-images.githubusercontent.com/79405382/108625918-6ee7ee80-7488-11eb-892c-633a7d8fbde6.png)
> System Architecture of Smart Temperature Logger:

![Picture2](https://user-images.githubusercontent.com/79405382/108625947-98087f00-7488-11eb-9d34-584bb70e0adb.png)
### How the Web Application looks like:
> Login Page:

![Picture3](https://user-images.githubusercontent.com/79405382/108626016-00576080-7489-11eb-9dc8-51c3b705b1e7.png)
> Dashboard (A)

![Picture4](https://user-images.githubusercontent.com/79405382/108626023-0a795f00-7489-11eb-88ba-29f8973ff7f7.png)
> Dashboard (B)

![Picture5](https://user-images.githubusercontent.com/79405382/108626025-0baa8c00-7489-11eb-8018-a7eac66356ce.png)
## Section 2 - Hardware Requirements
### Hardware Checklist
#### x1 Raspberry Pi 3 Model B
![image](https://user-images.githubusercontent.com/79405382/108626271-43660380-748a-11eb-8c10-52e5e2e295ed.png)
#### x1 Arduino Uno
![image](https://user-images.githubusercontent.com/79405382/108626546-a2784800-748b-11eb-9a09-c1b6946a64b8.png)
#### x1 T-Cobbler Plus for Raspberry Pi
![image](https://user-images.githubusercontent.com/79405382/108626338-9fc92300-748a-11eb-9e01-263f8f2e7a1c.png)
#### x1 I2C LCD 16x2 Screen
![image](https://user-images.githubusercontent.com/79405382/108626418-fb93ac00-748a-11eb-8886-b5edd3fee03d.png)
#### x1 RFID / NFC MFRC522 Card Reader Module
![image](https://user-images.githubusercontent.com/79405382/108626442-2978f080-748b-11eb-8881-4727773ed618.png)
#### x1 MLX90614 Infrared Temperature Sensor
![image](https://user-images.githubusercontent.com/79405382/108626453-3a296680-748b-11eb-8c4a-73087d284a58.png)
#### x1 HC-SR104 Ultrasonic Sensor
![image](https://user-images.githubusercontent.com/79405382/108626464-4d3c3680-748b-11eb-878e-6716407c8e9f.png)
#### x1 HW-279 2 Channel 5V Relay Module
![image](https://user-images.githubusercontent.com/79405382/108626487-62b16080-748b-11eb-95ff-331905eea2a9.png)
#### x1 9V Battery
![image](https://user-images.githubusercontent.com/79405382/108626503-76f55d80-748b-11eb-8e27-b3fd727ca3b5.png)
#### Jumper Cables
![image](https://user-images.githubusercontent.com/79405382/108626522-85dc1000-748b-11eb-9bcd-bbeecf38ab23.png)

## Section 3 - AWS/Hardware Setup
> Fritzing Diagram

![Picture6](https://user-images.githubusercontent.com/79405382/108626632-19addc00-748c-11eb-8754-d4918cfad746.png)

## Section 4 - Software Setup

#### Install AWS Python Library On Raspberry Pi
On RaspberryPi and EC2 , install the following: <br /> _sudo pip install --upgrade --force-reinstall pip==9.0.3_ <br /> _sudo pip install AWSIoTPythonSDK --upgrade --disable-pip-version-check_ <br /> _sudo pip install --upgrade pip_
#### Install Boto
On RaspberryPi and EC2 , run : <br /> _sudo pip install botocore_ <br /> _sudo pip install botocore --upgrade_ <br />
_sudo pip install boto3 --upgrade_ <br />
#### Install paho
On RaspberryPi and EC2 , run : <br /> _sudo pip install paho-mqtt_
#### Install AWS CLI On Raspberry Pi
On RaspberryPi, run : <br /> _sudo pip install awscli_ <br /> _sudo pip install awscli --upgrade_
#### Install telepot
On RasbperryPi , run : <br /> _sudo pip install telepot

#### Install Putty
Download [Putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)
#### Install WinSCP
Download [WinSCP](https://winscp.net/eng/download.php)

## Section 5 - AWS/Create a “Thing”
#### Setting Up Your “Thing”
a) First, navigate to IoT Core within the AWS website by clicking on services, then IoT Core.

![image](https://user-images.githubusercontent.com/79405382/108626671-5aa5f080-748c-11eb-8e26-1ae82365e9bf.png)

b) Under manage, select things and choose register a thing.

![image](https://user-images.githubusercontent.com/79405382/108626686-68f40c80-748c-11eb-8fe4-061a33a0fed2.png)

c) Choose Create a single thing.

![image](https://user-images.githubusercontent.com/79405382/108626699-7a3d1900-748c-11eb-9d92-b1795ed492f7.png)

d) Enter a name for your thing, for example, TempLogger. Leave the rest of the fields by their default values. Click next.

![image](https://user-images.githubusercontent.com/79405382/108626838-47475500-748d-11eb-9e46-879d09e54ae9.png)

e) Click create certificate. After a few seconds, the following page will appear. Download all four files. As for the root CA, download the VeriSign Class 3 Public Primary G5 root CA certificate file.

![image](https://user-images.githubusercontent.com/79405382/108626842-4f06f980-748d-11eb-910a-d856fbf7441e.png)
![image](https://user-images.githubusercontent.com/79405382/108626848-5a5a2500-748d-11eb-8b0e-815745c71ec2.png)
![image](https://user-images.githubusercontent.com/79405382/108626857-61813300-748d-11eb-8791-df9a2bbc6ce0.png)

f) Once done, rename the four files accordingly.

![image](https://user-images.githubusercontent.com/79405382/108626867-68a84100-748d-11eb-8143-4143af37a091.png)
![image](https://user-images.githubusercontent.com/79405382/108626869-6ba33180-748d-11eb-9cb1-1034170cfb1d.png)

g) Move these four files into a directory in the raspberry pi and EC2.

h) Click activate.

![image](https://user-images.githubusercontent.com/79405382/108626885-7a89e400-748d-11eb-95f2-0521067aa7fb.png)

i) Click register thing. You will create a policy later.

![image](https://user-images.githubusercontent.com/79405382/108626897-82498880-748d-11eb-9597-e7d64e6632dc.png)

j) Navigate to policies under the secure section. Click create a policy.

![image](https://user-images.githubusercontent.com/79405382/108626903-8a092d00-748d-11eb-95cf-bd2aee20f854.png)

k) Enter a name for your policy, for example, TempLoggerPolicy and enter the following under Add statements

![image](https://user-images.githubusercontent.com/79405382/108626945-d48aa980-748d-11eb-9840-cef6fac6344b.png)

l) Navigate to certificates under secure section. Select the certificate you created previously, and click attach policy. Attach the policy you created previously.

![image](https://user-images.githubusercontent.com/79405382/108626954-e0766b80-748d-11eb-9856-85f1930c531c.png)
![image](https://user-images.githubusercontent.com/79405382/108627076-b6717900-748e-11eb-86e0-7e1d768ada92.png)

m) Select the certificate you created previously again, and click attach thing. Attach the policy you previously created. Attach the thing you created previously.

![image](https://user-images.githubusercontent.com/79405382/108627061-9a6dd780-748e-11eb-8175-bb35ee00031d.png)

## Section 6 - AWS/DynamoDB Setup
#### DynamoDB 
a) First, navigate to DynamoDB within the AWS website by clicking on services, then DynamoDB. Click create table.

![image](https://user-images.githubusercontent.com/79405382/108627289-b756da80-748f-11eb-85c1-88fa7c488eb6.png)

b) Enter the table name “temp_hist”, the primary key “deviceid” and sort key "date_time" then click create.

![image](https://user-images.githubusercontent.com/79405382/108627374-28968d80-7490-11eb-9f4f-f24ecfd454d8.png)

c) Enter the table name “ambient_temp”, the primary key “deviceid” and sort key "date_time" then click create.

![image](https://user-images.githubusercontent.com/79405382/108627400-5a0f5900-7490-11eb-83f4-f34f77da6678.png)

d) Next, navigate back to IoT Core within the AWS website by clicking on services, then IoT Core. Click Act, then create button at the top right corner.

![image](https://user-images.githubusercontent.com/79405382/108627428-85924380-7490-11eb-95cb-92ff98812ceb.png)

e)In the AWS IoT console, in the left navigation pane, choose “Act”, then “Create a rule” for "MyTempRule"
* Name the rule and add description (optional)
* For Rule Query statement :
* SELECT * FROM 'sensors/temp'
* Set action by choosing "Add action"
* Configure action and choose "Split Message into multiple columns of a DynamoDB table)
* It will look like
![image](https://user-images.githubusercontent.com/79405382/108627531-0bae8a00-7491-11eb-9698-b9c660d57de7.png)


f)Create a second rule for "MyAmbientRule"
* Name the rule and add description (optional)
* For Rule Query statement :
* SELECT * FROM 'sensors/temp'
* Set action by choosing "Add action"
* Configure action and choose "Split Message into multiple columns of a DynamoDB table)
* It will look like
![image](https://user-images.githubusercontent.com/79405382/108627623-955e5780-7491-11eb-8962-500d8dcf3bae.png)

*** Remember to enable the rules

#### REST API endpoint of your “Thing”
a) Navigate to Things under Manage section in AWS IoT Core and select the thing you previously created

![image](https://user-images.githubusercontent.com/79405382/108627675-d35b7b80-7491-11eb-8550-f8eeb94888bc.png)

b) Take note of the string under HTTPS. You will need it later for some of the python codes.

## Section 7 - AWS/Simple Notification System
#### Creating Subscription Topic
a) Access the Amazon SNS console click on Get Started

![Picture7](https://user-images.githubusercontent.com/79405382/108628980-c42bfc00-7498-11eb-8d21-06c232d4fcda.png)

b) Choose Topics

![image](https://user-images.githubusercontent.com/79405382/108629015-ecb3f600-7498-11eb-9578-8e07efa7f404.png)

c) Choose New Topics

![image](https://user-images.githubusercontent.com/79405382/108629027-f9d0e500-7498-11eb-8bb3-7cf7f043d62b.png)

d) Create a topic called "EmployeeTopic" and take note of the ARN.

![image](https://user-images.githubusercontent.com/79405382/108629077-3270be80-7499-11eb-948e-1bb1ce10f347.png)

e) In the Amazon SNS console, select the check box next to the topic you just created. From the Actions menu, choose Subscribe to topic.

![image](https://user-images.githubusercontent.com/79405382/108629100-5df3a900-7499-11eb-847b-05b4406d9b25.png)

f) On Create subscription, from the Protocol drop-down list, choose SMS. In the Endpoint field, type your email address and then choose Create subscription.

![image](https://user-images.githubusercontent.com/79405382/108629139-88456680-7499-11eb-9d90-258aa2b21a25.png)

g) You will receive an email that confirms you successfully created the subscription. Click on the link to confirm subscription.

![image](https://user-images.githubusercontent.com/79405382/108629162-9d21fa00-7499-11eb-9c15-d8fa8c0a151b.png)

#### Creating IOT Rule for SNS to send email

In the AWS IoT console, in the left navigation pane, choose “Act”, then “Create a rule” for "EmployeeTempAlert"
* Name the rule and add description (optional)
* For Rule Query statement :
* SELECT * FROM 'sensors/temp' WHERE temperature >= 37.6
* Set action by choosing "Add action"
* Configure action and choose "Send a message as an SNS push notification" and choose the previously created subscription topic.
* It will look like
![image](https://user-images.githubusercontent.com/79405382/108629264-13bef780-749a-11eb-966c-97c86530b329.png)

*** Remember to enable the rules

## Section 8 - AWS/EC2 Hosting of Web Application

We used AWS EC2 to host our TempLogger web application. The following instructions demonstrate how to create, connect to and host the web application on the EC2 instance.

#### Creation of EC2 Instance
a) Go to EC2

b) Make sure server is on US East (N. Virginia)

c) Launch Instance

d) Choose a Amazon Machine Image (AMI) <br /> We choose Amazon Linux 2 AMI 64-bit (x86).

e) For instance type, choose t2.mirco

f) Then click “Next: Configure Instance Details”

g) Enable "Auto-assign Pubic IP"

h) Scroll till "Advanced Details and enter the follwing : <br /> 
_sudo yum check-update_ <br /> 
_sudo yum install -y amazon-linux-extras_ <br /> 
_sudo amazon-linux-extras enable python3.8_ <br /> 
_sudo yum clean metadata_ <br /> 
_sudo yum install python38 -y_ <br /> 

i) Add sufficient storage

j) Add relevant tags <br /> We enter “Name” for the Key and “Python Web Server” as the Value

k) Configure security group <br /> We did it with the following settings <br /> ![image](https://user-images.githubusercontent.com/79405382/108627834-84faac80-7492-11eb-80f5-30f17db10240.png)

l) A SSH rule has by default been added for you so that you can SSH into the server later

m) We will add a second rule to allow HTTP traffic as well.

n) Click the “Add Rule” button. 

o) Select “Custom TCP”, enter Port as “8001” and Source as “Anywhere” then "Save rules"

p) Choose "Create a new key pair" and give it a name. <br /> We will use this to SSH into the EC2 server.

#### Connecting to EC2 Instance

To connect to and move the web application files into our EC2 instance, two third-party programs
are required. Firstly, PuTTY so that we can SSH into the instance to perform commands such as
running the python files. Secondly, WinSCP to secure copy the required web application files into the
instance.

a) Head over to the following two websites to download and install WinSCP and PuTTY.

https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
https://winscp.net/eng/download.php

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image060.png "Optional title")

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image061.png "Optional title")

b) Once you have installed both softwares, open PuTTYgen.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image062.png "Optional title")

c) Choose RSA, click load and browse to the .pem file that you download previously (the key
pair). Click ok on the “successfully imported” dialog box.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image063.png "Optional title")

d) Choose save private key and click yes on the warning. A .ppk file is now saved. You are
now ready to SSH into the instance that you’ve created.

![image](https://user-images.githubusercontent.com/79405382/108628382-909ba280-7495-11eb-9ea2-b0cc2b06a032.png)

e) In the EC2 management console, take note of the Public DNS value. In this case, it is ec2-
52 - 37 - 2 - 61.us-west-2.compute.amazonaws.com.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image065.png "Optional title")

f) The default user name of the instance we had created is ec2-user. Within PuTTY, enter the
host name, ec2-user@ec2- 52 - 37 - 2 - 61.us-west-2.compute.amazonaws.com.
(<user_name>@<public DNS>)

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image066.png "Optional title")

g) Next, navigate to connection, SSH then auth. Under private key file for authentication,
browse to the .ppk file you created previously.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image067.png "Optional title")

h) Click Open, then click yes on the PuTTY security alert. You should now be SSH in to the EC2
instance that you’ve created.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image068.png "Optional title")

i) Now open WinSCP. Enter the public DNS value under host name and ec2-user under host
name like so.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image069.png "Optional title")

j) Click advanced. navigate to authentication under SSH. Under private key file, browse to
the .ppk file that you created previously.

![image](https://user-images.githubusercontent.com/79405382/108628435-ec662b80-7495-11eb-8da6-be7565ee6251.png)

k) Click OK, save as a site and login. Click YES when the warning dialog pops up. You are now
connected to the instance.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image071.png "Optional title")

l) Create a new directory in the instance, named 'templogger'. Navigate into it and move the
necessary web application files (Refer to section 13 and the zip files for the code) and the
rootca.pem, public.pem.key, private.pem.key and certifcate.pem.crt downloaded
previously into it.

![image](https://user-images.githubusercontent.com/79405382/108628132-11f23580-7494-11eb-9be3-fcedc137c079.png)

#### Running the Web Application


a) Open the PuTTY connection that you established previously

b) Create a virtual environment for that folder:
``python3.8 -m venv ~/ec2/env``

c) Start the virtual environment and enter the respective directory:
``source ~/ec2/env/bin/activate``
``cd templogger``

d) Install the necessary components:
``pip3 install boto3 flask numpy AWSIoTPythonSDK``

e) Run "server.py"


## Section 9 - Raspberry Pi Configuration
#### Enable SPI and prepare the MFRC522 libraries

If your raspberry pi is not configured with the MFRC522 libraries, you can follow the following
instructions to set it up.

##### << Enable SPI via raspi-config >>


a) Run raspi-config, choose menu item “5 Interfacing Options” and enable SPI.

```
sudo rasp-config
```
![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image076.png "Optional title")

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image077.png "Optional title")

##### << Enable device tree in boot.txt>>

a) Modify the /boot/config.txt to enable SPI

```
sudo nano /boot/config.txt
```

b) Ensure these lines are included in config.txt

```
device_tree_param=spi=on
dtoverlay=spi-bcm2835
```

**<< Install Python-dev>>**
c) Install the Python development libraries

```
sudo apt-get install python-dev
```

**<< Install SPI-Py Library >>**

d) Set up the SPI Python libraries since the card reader uses the SPI interface
```
git clone https://github.com/lthiery/SPI-Py.git
cd /home/pi/SPI-Py
sudo python setup.py install
```

**<< Install RFID library >>**

e) Clone the MFRC522-python library and copy out the required files to your project directory
```
git clone https://github.com/rasplay/MFRC522-python.git
cd MFRC52 2 - python
sudo cp *.py ~/templogger
```
f) Edit the MFRC522.py file that you just cloned from GitHub.
```
sudo nano ~/temploggerk/MFRC522.py
```
g) Scroll down to the function “__init__” and make the following changes:

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image078.png "Optional title")

## Section 10 - Raspberry Pi Setup

a) Run main.py on the Raspberry Pi

## Section 11 - Arduino Setup

a) Connect your Arduino to Raspberry Pi

b) Upload the Arduino.ino codes into the arduino using Arduino IDE

## Section 12 - Expected Outcome

To test if the program works

* run server.py on the EC2 instance
* upload the arduino.ino code to the Arduino
* run main.py on the Raspberry Pi

The following is the link to the video demonstration of what the application should look like. <br />
https://youtu.be/xpzw3DpkwlU

There is a need to turn the Temperature System on from the Web Server. Access the webserver and log into the domain.

Turn on the Temperature System by clicking on the "ON/OFF" button on the dashboard. Once there is a message displayed on the LCD screen stating that the system is online, and everything should be in order.
