import socket
import threading
import RPi.GPIO as GPIO
import time
import datetime

def server():
    """
    Start a socket server and wait for the other RPi to connect
    """
    
    # Create a socket with IPv4 and TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('[SOCKET CREATED]')
    
    # Reserve port number
    port = 12345 

    # Bind any address to port number
    s.bind(('', port))

    # Socket is listening for clients
    # Max 1 client
    s.listen(1)
    print('- Listening for clients..')
    
    # Accept client and create a socket object and the associated IP
    client, addr = s.accept()
    print(f'[CLIENT CONNECTED] {addr}')
    
    thread_timer = threading.Timer(5, timer_led_2)
    while True:
        """
        This loop will handle data that is sent from client
        and control the actuators (led)
        """
        # Receive data from client with the temperature
        data = client.recv(1024)
        temp = data.decode()
        temp = temp[0:2]
        client_timestamp = ''
        timestamp = datetime.datetime.now().time() # To compare timestamps on packets
        print(f'- TEMPERATURE: {data.decode()} | {timestamp}')
        
        # Break if no data is received from client
        if not data:
            break
        # Check if temp >= 23 and turn on led 1
        elif float(temp) >= 22:
            led_1(state='on')
            print('Temp 23 or more, LED 1 on')
            
            # Start 5 second timer in a thread if no thread is running
            if not thread_timer.is_alive():
                thread_timer = threading.Timer(5, timer_led_2)
                thread_timer.start()
        else:
            # Temp under 23, turn off leds
            # If thread is_alive break the thread
            if thread_timer.is_alive():
                # If its alive cancel thread
                thread_timer.cancel()
                print('- Temp under 23, turning off LEDs')
                led_2(state='off')
            
            # Make sure LEDs is off
            led_2(state='off')                             
            led_1(state='off')
    
    # Close connections and make sure led is off
    led_1(state='off')
    led_2(state='off')
    client.close()
    s.close()


def timer_led_2():
    """
    Starts if thread timer reaches five seconds and turns on LED 2
    """
    print('- 5 seconds over 23 degrees, LED 2 on')
    led_2(state='on')


def led_1(state='off'):
    """
    LED 1 start within 2 seconds after temp > 23
    LED 2 start within 1 second after temp > 23 CONTINUOSLY FOR 5 seconds
    USING GPIO-PIN 17
    """
    # Set pin to BCM board
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup pin 17 initial to 0V
    GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
    # If state is on, turn on LED
    if state == 'on':
        GPIO.output(17, GPIO.HIGH)
    # Else turn off LED and cleanup
    else:
        GPIO.output(17, GPIO.LOW)
        GPIO.cleanup()


def led_2(state='off'):
    """
    USING GPIO-PIN 23
    """
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
        server()
    except KeyboardInterrupt:
        led_1(state='off')
        led_2(state='off')
        exit()

