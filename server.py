import network
import socket
from secrets import SSID, PASSWORD
import displayController
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from httpParser import HttpParser

displayController = displayController.DisplayController()
buzzer = machine.PWM(machine.Pin(16))
buzzer.freq(500)


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    counter = 0
    wait = 1
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        print(f'Trying to connect to {SSID}...')
        for _ in range(10):
            if wlan.isconnected():
                break
            counter += wait
            print(f'waiting for connection... {counter} seconds')
            sleep(wait)
        else:
            print('Connection attempt failed. Trying again.\n')
            return connect()
        ip = wlan.ifconfig()[0]
        print(f'Connected on {ip}')
        return wlan.ifconfig()[0]
    else:
        return wlan.ifconfig()[0]        


def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, state):
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            
            <p>Phico me! :)</p>
            
            <form>
            <label>Enter Username (max 16 chars)</label>
            <input type="text" name="username" id="username"/>
            <p></p>
            <label>Enter Message (max 100 chars)</label>
            <input type="text" name="msg" id="msg"/>
            <input type="submit" name="submit" id="submit"/>
            </form>

            <p>CPU temperature is {temperature}</p>

            </body>
            </html>
            """
    return str(html)

def buzz():
    buzzer.duty_u16(1000)
    sleep(0.2)
    buzzer.duty_u16(0)
    sleep(0.1)
    buzzer.duty_u16(1000)
    sleep(0.2)
    buzzer.duty_u16(0)

def serve(connection):
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        #result = HttpParser.parse(request)
        #print(request)
        try:
            rawData = request.split()
            rawMsg = rawData[1].split('&')
            username = rawMsg[0].split('=')[1]
            msg = rawMsg[1].split('=')[1]
            msg = msg.replace('+',' ')
            msg = msg.replace('%3F','?')
            msg = msg.replace('%21','!')
            msg = msg.replace('%2C',',')
            msg = msg.replace('%3A', ':')
            msg = msg.replace('%E4', 'ä')
            #print(rawMsg[0].split('=')[0])
            print(username+": "+msg)
            if(rawMsg[0].split('=')[0] == '/?username'): # quick hack to sort out random unrelated requests
                buzz()
                displayController.add_message(msg,username)
        except IndexError:
            pass 
        
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()

if __name__=="__main__":
    
    try:
        ip = connect()
        connection = open_socket(ip)
        print('Now serving!')
        serve(connection)
    except KeyboardInterrupt:
        try:
           connection.close()
        except NameError:
            print("socket not found. didnt close.")
        wlan.disconnect()
        wlan.active(False)
        flushinput()
        machine.reset()
