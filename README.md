# piStatus
 Raspberry Pi Status Monitor with SSD1306 OLED Screen and Fan Control

This project is under development.

**HOW TO USE IT**
Install required library for git

    sudo apt-get install git

Clone it from github.

    cd ~
    git clone https://github.com/erdemarslan/piStatus.git
    cd piStatus

Install required modules.

    pip3 install -r requirement.txt

Enable I2C from Raspberry Configuration and Reboot your RPI.

Run the code

    cd ~/piStatus
    python3 pistatus.py

If you want it start on Raspberry Pi Startup you must do that.
Open terminal.

    sudo nano /etc/local.rc

Add this line before exit(0)

    sudo python3 /home/pi/piStatus/pistatus.py &

Save and reboot your RPI.
