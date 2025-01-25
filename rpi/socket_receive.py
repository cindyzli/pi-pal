import socket
import json
import RPi.GPIO as GPIO
from gpiozero import Buzzer
from time import sleep

LED_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set LED pin as output
GPIO.setup(LED_PIN, GPIO.OUT)
# Create PWM object with frequency 50Hz
pwm = GPIO.PWM(LED_PIN, 50)
# Start PWM with initial duty cycle 50%
pwm.start(50)

buzzer = Buzzer(17)

# Function to handle the incoming command
def handle_command(command):
    print(f"Received command: {command}")
    if command["action"] == "adjust_led":
        brightness = command["brightness"]
        pwm.ChangeDutyCycle(brightness)
        print(f"Set LED brightness to {brightness}%")
    if command["action"] == "sound_buzzer":
        buzzer.on()
        sleep(5)
        buzzer.off()
        

# Set up the server to keep listening for connections
def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Listening for incoming connections on {host}:{port}...")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)  # Receive data from the client
                if data:
                    try:
                        command = json.loads(data.decode('utf-8'))  # Parse the JSON data
                        handle_command(command)  # Process the command
                    except json.JSONDecodeError:
                        print("Received invalid JSON data")
                else:
                    print("No data received")
            # After handling the command, continue listening

if __name__ == "__main__":
    raspberry_pi_ip = "0.0.0.0"  # Listen on all interfaces
    raspberry_pi_port = 12345    # Port to listen on
    start_server(raspberry_pi_ip, raspberry_pi_port)