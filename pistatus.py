#!/usr/bin/python3
# Libraries
from gpiozero import CPUTemperature, LoadAverage
import time
from threading import Timer
import netifaces
import psutil
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import datetime

# Variables
network = "wlan0"
IP = "0.0.0.0"
netmask = "0.0.0.0"
gateway = "0.0.0.0"
number = 0
cpu_temp_total = 0
cpu_percent_total = 0
mem_total = 0
mem_used_total = 0
mem_available_total = 0
mem_used = 0
mem_available = 0
cpu_temp = 0
cpu_percent = 0
fan_speed = 100
screen_no = -1
disk_total = 0
disk_used = 0
disk_free = 0
disk_percent = 0
date_text = "01.01.1970"
time_text = "00.00.00"
weekday_text = "Sunday"
RST = None

# Loading Classes
cpu = CPUTemperature()
loadAvarage = LoadAverage(min_load_average=0, max_load_average=2, minutes=1)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize display.
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
#image = Image.open("./icon/temperature.bmp").convert("1")
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.truetype('/home/pi/piStatus/icon/Ubuntu-R.ttf', 12)

# Getting IP Address
def getIPAddress():
    global IP
    global netmask
    global gateway
    global network

    try:
        IP = netifaces.ifaddresses(network)[2][0]['addr']
        netmask = netifaces.ifaddresses(network)[2][0]['netmask']
        gateway = netifaces.gateways()['default'][2][0]
    except:
        pass
    t = Timer(30, getIPAddress)
    t.start()

# Get IP Address
getIPAddress()

def calculate_cpu():
    global number
    global cpu_temp_total
    global cpu_percent_total
    global cpu_temp
    global cpu_percent
    global mem_total
    global mem_used
    global mem_available
    global disk_total
    global disk_used
    global disk_free
    global disk_percent

    mem_total = psutil.virtual_memory()[0] / (2**30) # GB
    mem_used = psutil.virtual_memory()[3] / (2**30) # GB
    mem_available = psutil.virtual_memory()[1] / (2**30) # GB

    disk_used = psutil.disk_usage('/')[1] / (2**30) #GB
    disk_free = psutil.disk_usage('/')[2] / (2**30) #GB
    disk_total = psutil.disk_usage('/')[0] / (2**30) #GB
    disk_percent = psutil.disk_usage('/')[3] #GB

    if number < 10:
        cpu_temp_total += cpu.temperature
        cpu_percent_total += psutil.cpu_percent()
        number += 1
    else:
        cpu_temp = cpu_temp_total / 10
        cpu_percent = cpu_percent_total / 10
        number = 0
        cpu_temp_total = 0
        cpu_percent_total = 0

    t = Timer(0.1, calculate_cpu)
    t.start()

calculate_cpu()

def get_date_time():
    global date_text
    global time_text
    global weekday_text
    now = datetime.datetime.now()
    date_text = now.strftime("%d.%m.%Y")
    time_text = now.strftime("%H.%M.%S")
    weekday_text = now.strftime("%A")
    t = Timer(1, get_date_time)
    t.start()

get_date_time()

def raise_screen_no():
    global screen_no
    screen_no += 1
    if screen_no > 4:
        screen_no = 0
    t = Timer(5, raise_screen_no)
    t.start()

raise_screen_no()

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)


    if screen_no == 1:
        image = Image.open("/home/pi/piStatus/icon/temperature.bmp").convert("1")
        draw = ImageDraw.Draw(image)

        var_temp = "{0:.2f} C".format(cpu_temp)
        var_cpu_load = "{0:.2f} %".format(cpu_percent)
        var_fan_speed = "Fan Speed: {0}%".format(fan_speed)

        draw.text((x+20, top+4), "CPU Information   ",  font=font, fill=255)
        draw.text((x+55, top+20), var_temp, font=font, fill=255)
        draw.line((x+50, top+36, x+100, top+36), fill=255)
        draw.text((x+55, top+36), var_cpu_load, font=font, fill=255)
        draw.text((x+20, top+52), var_fan_speed, font=font, fill=255)

    elif screen_no == 2:
        image = Image.open("/home/pi/piStatus/icon/network.bmp").convert("1")
        draw = ImageDraw.Draw(image)

        draw.text((x, top+4), "  Network Information  ",  font=font, fill=255)
        draw.text((x+55, top+20), str(IP), font=font, fill=255)
        draw.text((x+55, top+36), str(netmask), font=font, fill=255)
        draw.text((x+55, top+52), str(gateway), font=font, fill=255)

    elif screen_no == 3:
        image = Image.open("/home/pi/piStatus/icon/memory.bmp").convert("1")
        draw = ImageDraw.Draw(image)

        var_mem_total = "T: {0:.2f} GB".format(mem_total)
        var_mem_used = "U: {0:.2f} GB".format(mem_used)
        var_mem_available = "F: {0:.2f} GB".format(mem_available)

        draw.text((x+20, top+4), "RAM Information  ",  font=font, fill=255)
        draw.text((x+55, top+20), var_mem_used, font=font, fill=255)
        draw.text((x+55, top+36), var_mem_available, font=font, fill=255)
        draw.text((x+55, top+52), var_mem_total, font=font, fill=255)

    elif screen_no == 4:
        image = Image.open("/home/pi/piStatus/icon/disk.bmp").convert("1")
        draw = ImageDraw.Draw(image)

        var_disk_total = "T: {0:.2f} GB".format(disk_total)
        var_disk_used = "U: {0:.2f} GB".format(disk_used)
        var_disk_free= "F: {0:.2f} GB".format(disk_free)
        var_disk_percent = "{0:.2f}%".format(disk_percent)


        draw.text((x+20, top+4), "Disk Information  ",  font=font, fill=255)
        draw.text((x+55, top+20), var_disk_used, font=font, fill=255)
        draw.text((x+55, top+36), var_disk_free, font=font, fill=255)
        draw.text((x+55, top+52), var_disk_total, font=font, fill=255)
        draw.text((x+10, top+52), var_disk_percent, font=font, fill=255)

    else:
        image = Image.open("/home/pi/piStatus/icon/time.bmp").convert("1")
        draw = ImageDraw.Draw(image)

        draw.text((x+35, top+4), "Date - Time  ",  font=font, fill=255)
        draw.text((x+55, top+20), date_text, font=font, fill=255)
        draw.text((x+55, top+36), time_text, font=font, fill=255)
        draw.text((x+55, top+52), weekday_text, font=font, fill=255)


    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)
