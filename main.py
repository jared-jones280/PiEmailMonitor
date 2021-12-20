import os
from dotenv import load_dotenv
from imapclient import IMAPClient
import email

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

def getMessages(host,user,password):
    m = []
    #create server, login, and search inbox for messages
    server = IMAPClient(host, use_uid=True, ssl=ssl)
    server.login(user, password)
    server.select_folder("INBOX")
    messages = server.search([['NOT','DELETED'], [u'FLAGGED']])

    #get most recent messages [-1] (last item in list) and print info
    for uid, message_data in server.fetch(messages, "RFC822").items():
            email_message = email.message_from_bytes(message_data[b"RFC822"])

            #write subject line to file
            #Debugging email content v
            #print(uid, email_message.get("From"))
            #print("Subject: ",email_message.get("Subject"))
            #print("Body: \n",email_message.get_payload()[0])

            subject = email_message.get("Subject")
            m.append(subject)

    server.logout()
    return m

    

if __name__ == "__main__":

    #SETUP FOR MAIL CLIENT
    load_dotenv()
    #now have access to uid and pass and monitoremail
    #login to email server and setup
    host = 'imap.gmail.com'
    user = os.getenv("uid")
    password = os.getenv("pass")
    ssl = True

    #SETUP FOR DISPLAY
    # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = None

    # Config for display baudrate (default max is 24mhz):
    BAUDRATE = 64000000

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()

    # Create the ST7789 display:
    disp = st7789.ST7789(
        spi,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=BAUDRATE,
        width=240,
        height=240,
        x_offset=0,
        y_offset=80,
    )
    #create buttons
    buttonA = digitalio.DigitalInOut(board.D23)
    buttonB = digitalio.DigitalInOut(board.D24)
    buttonA.switch_to_input()
    buttonB.switch_to_input()
    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
    image = Image.new("RGB", (width, height))
    rotation = 0

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image, rotation)
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the
    # same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

    # Turn on the backlight
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    backlight.value = True

    messages = getMessages(host,user,password)
    #print(messages)
    leng = len(messages)
    iter = leng-1
    idleCount = 0

    while True:
        #print(idleCount)
        #if(idleCount % 10 == 0):
        #   print('10 seconds passed w/ no input')
        
        #check if any button inputs in last 30 seconds
        if(idleCount == 30):
            backlight.value = False
            #if button press stop waiting, fetch new messages, turn on display
            while(True):
                if not buttonA.value:
                    break
                if not buttonB.value:
                    break
            #print('checking for new messages')
            messages = getMessages(host,user,password)
            #print(messages)
            leng = len(messages)
            iter = leng-1
            idleCount == 0
            backlight.value = True

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        #check button values
        if not buttonA.value:
            if iter >0:
                iter -= 1
                #print("buttonA press")
                idleCount = 0
        if not buttonB.value:
            if iter+1 < leng:
                iter += 1
                #print("buttonB press")
                idleCount = 0
        # Shell scripts for system monitoring from here:
        # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d' ' -f1"
        IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
        #cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        #CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
        #cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
        #MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
        #cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
        #Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
        #cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
        #Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

        #COLORS
        White = "#FFFFFF"
        Pink = "#F52FE4"
        LightBlue = "#2DE0F7"
        DarkBlue = "#0F22F2"
        Yellow = "#FCF005"
        Green = "#0DFC05"

        #INFOTXT
        status = "Message: "+ str(iter+1) + "/" + str(leng)

        #Dividing Message
        lines = messages[iter].split('#')
        while(len(lines)<5):
            lines.append(' ')

        # Plan lines of text.
        y = top
        # Lauren,
        l1= "Lauren, "
        draw.text((x, y), l1, font=font, fill=White)
        y += font.getsize(l1)[1]
        # <Message>
        draw.text((x, y), lines[0], font=font, fill=White)
        y += font.getsize(lines[0])[1]
        # <Message> //spacer?
        space = " "
        draw.text((x, y), lines[1], font=font, fill=White)
        y += font.getsize(lines[1])[1]
        # <Message> //spacer?
        draw.text((x, y), lines[2], font=font, fill=White)
        y += font.getsize(lines[2])[1]
        # <Message> //spacer?
        draw.text((x, y), lines[3], font=font, fill=White)
        y += font.getsize(lines[3])[1]
        # <Message> //spacer?
        draw.text((x, y), lines[4], font=font, fill=White)
        y += font.getsize(lines[4])[1]
        # Message: ##/##
        draw.text((x, y), status , font=font, fill=White)
        y += font.getsize(status)[1]
        # IP: xxx.xxx.x.x
        draw.text((x, y), IP, font=font, fill=White)
        y += font.getsize(IP)[1]
        # <- Left Right -> A, B
        inst = "    v Prev | Next ^"
        draw.text((x, y), inst, font=font, fill=White)
        y += font.getsize(inst)[1]

        #Lines of text
        #y = top
        #draw.text((x, y), IP, font=font, fill="#FFFFFF")
        #y += font.getsize(IP)[1]
        #draw.text((x, y), CPU, font=font, fill="#FFFF00")
        #y += font.getsize(CPU)[1]
        #draw.text((x, y), MemUsage, font=font, fill="#00FF00")
        #y += font.getsize(MemUsage)[1]
        #draw.text((x, y), Disk, font=font, fill="#0000FF")
        #y += font.getsize(Disk)[1]
        #draw.text((x, y), Temp, font=font, fill="#FF00FF")

        # Display image.
        disp.image(image, rotation)
        idleCount += 1
        time.sleep(0.1)
