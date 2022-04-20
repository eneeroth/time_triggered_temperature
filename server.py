import socket
import threading
import RPi.GPIO as GPIO
import time
import datetime

def start_server():
    """
    Start the server and wait for the other RPi to connect
    """
    
    # Create a socket with IPv4 and TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('- Socket created')
    
    # Reserve port number
    port = 12345 

    # Bind any address to port number
    s.bind(('', port))

    # Socket is listening for clients
    # Max 1 clients
    s.listen(1)
    print('- Listening for clients..')
    
    # Accept client and crate a socket object and the associated IP
    client, addr = s.accept()
    print(f'- {addr} connected')
    
    thread_running = False
    thread = threading.Thread(target=timer)
    while True:
        # Receive data from client with the temperature
        data = client.recv(1024)
        print(datetime.datetime.now().time())
        print(f'TEMPERATURE: {data.decode()}')
        
        if not data:
            break
        elif float(data.decode()) >= 23:
            # Turn on led
            led_1(state='on')
            
            # Start 5 second timer
            if not thread_running:
                thread = threading.Thread(target=timer)
                thread_running = True
                thread.start()
        else:
            # Temp under 23, turn off leds
            thread_running = False
            #print(thread.is_alive())
            if thread.is_alive():
                print('- Temp under 23')
                thread.join()
                thread_running = False
                led_2(state='off')

            led_2(state='off')                             
            led_1(state='off')
    
    # Close connections
    led_1()
    client.close()
    s.close()


def timer():
    """
    Start a 5 second timer and if timer runs out start led 2
    """
    time.sleep(5)
    print('- 5 seconds over 23 degrees')
    led_2(state='on')


def led_1(state='off'):
    """
    LED 1 start within 2 seconds after temp > 23
    LED 2 start within 1 second after temp > 23 CONTINUOSLY FOR 5 seconds
    """
    # Set pin to BCM board
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup pin 17 initial to 0V
    GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
    # If stan is on, turn on LED
    if state == 'on':
        GPIO.output(17, GPIO.HIGH)
    # Else turn off LED and cleanup
    else:
        GPIO.output(17, GPIO.LOW)
        GPIO.cleanup()


def led_2(state='off'):
    # Set pin to BCM board
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup pin 17 initial to 0V
    GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
    # If stan is on, turn on LED
    if state == 'on':
        GPIO.output(23, GPIO.HIGH)
    # Else turn off LED and cleanup
    else:
        GPIO.output(23, GPIO.LOW)
        GPIO.cleanup()


if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        exit()

