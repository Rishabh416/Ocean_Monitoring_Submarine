# Research Project for Ocean Monitoring
This project works on creating a ocean monitoring submarine. The system is equipped with a Raspberry Pi 4 Model B which is able to capture live video feed through an Arducam 5MP camera. The Raspberry Pi uses the Picamera2 library to interface with the camera. The live video feed is displayed on a webUI which also facilitates a 9-key control system to maneuver the submarine. 

## Hardware
Raspberry Pi 4 Model B
Arducam 5MP OV5647

## Software
- FastAPI: This library is used to provide API access points that can be accessed by the webUI to display a live camera feed and relay information
- Uvicorn: This library is a web server which is being used to host the API endpoints on a local host. 
- Picamera2: This library is used to interface with the camera and capture images.
- OpenCV: This library is for image processing and used to encode/decode the images so that it can be relayed over an API endpoint. 
- Time: This library is used to get access to the current time and provide a unique identifier to each image saved. 

## Initial Setup (Windows)
**Installing Raspberry PI OS**
- Install the Raspberry Pi Imager (https://www.raspberrypi.com/software/) for Windows
- Connect a microSD card to your laptop/PC, launch the Raspberry Pi Imager and select the below options for the respective fields, click **NEXT**
    - CHOOSE DEVICE: Raspberry Pi 4
    - CHOOSE OS: Raspberry Pi OS (64-bit)
    - CHOOSE STORAGE: *the displayed microSD card*
- When prompted for OS Customization, select **EDIT SETTINGS**, add in the below details for their respective fields and then click **Save**
    - General
        - Set hostname: pi.local
        - Set username and password: *Select your own username and password*
        - Configure wireless LAN: SSID should be your Wi-Fi network name, Password should be your Wi-Fi network password, Wireless LAN country should be set as appropriate to your Wi-Fi network location
        - Set locale settings: *Adjust settings as appropriate to your location*
    - Services
        - Enable SSH: Yes
        - Select: Use password authentication
- Follow the prompted instructions to write the OS to the microSD card

**SSH into the Raspberry PI**
- Open a Terminal window on your laptop/PC and enter ```ssh {username}@pi.local```, alternatively you can replace pi.local with the IP address of the Raspberry Pi (can be accessed through your routers admin page)
- Enter your password and you should be able to SSH into the Raspberry PI

**Boot settings for Arducam 5MP OV5647**
- Run the following command ```sudo nano /boot/firmware/config.txt```
- Find the line mentioning **camera_auto_detect** and set its value to **0**
- Go to the bottom of the file (below \[all\]) and add the following line under **dtoverlay=ov5647**
- Click **Ctrl + X** to exit, click **Y** to save changes, click **Enter** to save and exit the file

## Ethernet Networking Setup (Windows)
**On Windows PC/Laptop**
- Open Windows Network Connections by clicking  **Win + R** and then typing **ncpa.cpl**
- Right click on the **Ethernet** option and select **properties**
- Set a static IP by selecting **TCP/IPv4** then **properties**, add the following details in their respective fields, leaving the rest blank, and then click **ok**
    - IP Address: 192.168.1.1
    - Subnet mask: 255.255.255.0

**On Raspberry PI**
- Install dhcpcd using the following commands ```sudo apt update```, ```sudo apt install dhcpcd5```
- Enable dhcpcd using the following commands ```sudo systemctl start dhcpcd```, ```sudo systemctl enable dhcpcd```
- Configure the network on the Raspberry Pi by accessing the configuration file ```sudo nano /etc/dhcpcd.conf```
- Add the following lines at the end of the file and then run ```sudo service dhcpcd restart```
```
interface eth0
static ip_address=192.168.137.2/24
static routers=192.168.137.1
static domain_name_servers=192.168.137.1
```

**On Windows PC/Laptop**
- Open Windows Network Connections by clicking  **Win + R** and then typing **ncpa.cpl**
- Right click on the **Wi-Fi** option and select **properties**
- Go to the **sharing** tab and enable **Allow other network users to connect through this computer's Internet connection**

- Verify connectivity by running ```ping google.com``` on the Raspberry Pi
- Disable Wi-Fi on the Raspberry Pi by accessing ```sudo nano /boot/firmware/config.txt``` and adding ```dtoverlay=disable-wifi``` at the bottom of the file
