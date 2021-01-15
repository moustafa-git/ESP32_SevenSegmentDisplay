import machine
import time
incButton = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
decButton = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
resButton = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
a = machine.Pin(19,machine.Pin.OUT)
b = machine.Pin(21,machine.Pin.OUT)
c = machine.Pin(15,machine.Pin.OUT)
d = machine.Pin(23,machine.Pin.OUT)
e = machine.Pin(22,machine.Pin.OUT)
f = machine.Pin(5,machine.Pin.OUT)
g = machine.Pin(4,machine.Pin.OUT)
#led = machine.Pin(12,machine.Pin.OUT)
counter = 0
incFlag = 0
decFlag = 0
resFlag = 0

a.off()
b.off()
c.off()
d.off()
e.off()
f.off()
g.on()

# ************************
# Configure the ESP32 wifi
# as Access Point mode.
import network
ssid = 'ESP32'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
while not ap.active():
    pass
print('network config:', ap.ifconfig())


# ************************
# Configure the socket connection
# over TCP/IP
import socket

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
s.listen(5)     # max of 5 socket connections

# ************************
# Function for creating the
# web page to be displayed

def web_page():
    if incFlag == 0 :
        state_inc = '<span style="height:25px;width:25px;background-color:#bbb;border-radius:50%;display:inline-block;"></span>'
    if incFlag == 1 :
        state_inc = '<span style="height:25px;width:25px;background-color:red;border-radius:50%;display:inline-block;"></span>'
    if decFlag == 0 :
        state_dec = '<span style="height:25px;width:25px;background-color:#bbb;border-radius:50%;display:inline-block;"></span>'
    if decFlag == 1 :
        state_dec = '<span style="height:25px;width:25px;background-color:red;border-radius:50%;display:inline-block;"></span>'
    if resFlag == 0 :
        state_res = '<span style="height:25px;width:25px;background-color:#bbb;border-radius:50%;display:inline-block;"></span>'
    if resFlag == 1 :
        state_res = '<span style="height:25px;width:25px;background-color:red;border-radius:50%;display:inline-block;"></span>'
        
    html_page = """
<!DOCTYPE html>
<html>  
        <head>  
          <meta name="viewport" content="width=device-width, initial-scale=1">  
        </head>  
        <body id="test">  
           <center><h2>ESP32 SEVEN SEGMENT DISPLAY</h2></center>  
           <center>  
             <form>  
               <button type='submit' name="INC" value='0'> LED INC </button>  
               <button type='submit' name="DEC" value='0'> LED DEC </button>
               <button type='submit' name="RES" value='0'> LED RES </button>  
             </form>
           </center>
           <center>
               <p><strong>INC</strong></p>"""+state_inc+"""
                <p><strong>DEC</strong></p>"""+state_dec+"""
                <p><strong>RES</strong></p>"""+state_res+"""
            </center>  
        <script>
            setInterval(function(){loadDoc()}, 100);
            function loadDoc() {
              var xhttp = new XMLHttpRequest();
              xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                document.getElementById("test").innerHTML =
                  this.responseText;
                }
              };
              xhttp.open("GET", "HIII", true);
              xhttp.send();
            }
        </script>
        </body>  
        </html>"""
    return html_page

while True:
    firstInc = incButton.value()
    firstDec = decButton.value()
    firstRes = resButton.value()
    # Socket accept() 
    conn, addr = s.accept()
    print("Got connection from %s" % str(addr))
    
    # Socket receive()
    request=conn.recv(1024)
    print("")
    print("")
    print("Content %s" % str(request))

    # Socket send()
    request = str(request)
    thirdInc = request.find('/?INC=0')
    thirdDec = request.find('/?DEC=0')
    thirdRes = request.find('/?RES=0')
    
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    incFlag = 0
    decFlag = 0
    resFlag = 0
    # Socket close()
    conn.close()
    secondInc = incButton.value()
    secondDec = decButton.value()
    secondRes = resButton.value()
    
    if firstInc and not secondInc or thirdInc == 6:
        incFlag = 1
        #print('Button pressed!')
        counter = counter + 1
        if (counter > 9):
            counter = 0
        if (counter == 0):
            a.off()
            b.off()
            c.off()
            d.off()
            e.off()
            f.off()
            g.on()  
        if (counter == 1):
            a.on()
            b.off()
            c.off()
            d.on()
            e.on()
            f.on()
            g.on()
        if (counter == 2):
            a.off()
            b.off()
            c.on()
            d.off()
            e.off()
            f.on()
            g.off()
        if (counter == 3):
            a.off()
            b.off()
            c.off()
            d.off()
            e.on()
            f.on()
            g.off()
        if (counter == 4):
            a.on()
            b.off()
            c.off()
            d.on()
            e.on()
            f.off()
            g.off()
        if (counter == 5):
            a.off()
            b.on()
            c.off()
            d.off()
            e.on()
            f.off()
            g.off()
        if (counter == 6):
            a.off()
            b.on()
            c.off()
            d.off()
            e.off()
            f.off()
            g.off()
        if (counter == 7):
            a.off()
            b.off()
            c.off()
            d.on()
            e.on()
            f.on()
            g.on()
        if (counter == 8):
            a.off()
            b.off()
            c.off()
            d.off()
            e.off()
            f.off()
            g.off()
        if (counter == 9):
            a.off()
            b.off()
            c.off()
            d.off()
            e.on()
            f.off()
            g.off()
        thirdInc == 0
            
    if firstDec and not secondDec or thirdDec == 6:
        decFlag = 1
        #print('Button pressed!')
        counter = counter - 1
        if (counter < 0):
            counter = 9
        if (counter == 0):
            a.off()
            b.off()
            c.off()
            d.off()
            e.off()
            f.off()
            g.on()  
        if (counter == 1):
            a.on()
            b.off()
            c.off()
            d.on()
            e.on()
            f.on()
            g.on()
        if (counter == 2):
            a.off()
            b.off()
            c.on()
            d.off()
            e.off()
            f.on()
            g.off()
        if (counter == 3):
            a.off()
            b.off()
            c.off()
            d.off()
            e.on()
            f.on()
            g.off()
        if (counter == 4):
            a.on()
            b.off()
            c.off()
            d.on()
            e.on()
            f.off()
            g.off()
        if (counter == 5):
            a.off()
            b.on()
            c.off()
            d.off()
            e.on()
            f.off()
            g.off()
        if (counter == 6):
            a.off()
            b.on()
            c.off()
            d.off()
            e.off()
            f.off()
            g.off()
        if (counter == 7):
            a.off()
            b.off()
            c.off()
            d.on()
            e.on()
            f.on()
            g.on()
        if (counter == 8):
            a.off()
            b.off()
            c.off()
            d.off()
            e.off()
            f.off()
            g.off()
        if (counter == 9):
            a.off()
            b.off()
            c.off()
            d.off()
            e.on()
            f.off()
            g.off()
        thirdDec = 0

    if firstRes and not secondRes or thirdRes == 6:
        resFlag = 1
        counter = 0
        a.off()
        b.off()
        c.off()
        d.off()
        e.off()
        f.off()
        g.on()
        thirdRes = 0
