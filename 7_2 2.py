import speech_recognition as sr
import RPi.GPIO as GPIO
from tkinter import *
import threading

# Set up GPIO:
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Function to control the LED:
def control_led(command, led_status_label):
    if "on" in command.lower():
        GPIO.output(LED_PIN, GPIO.HIGH)
        led_status_label.config(text="Light is ON", fg="green")
    elif "off" in command.lower():
        GPIO.output(LED_PIN, GPIO.LOW)
        led_status_label.config(text="Light is OFF", fg="red")
    led_status_label.update()

# GUI setup:
def setup_gui():
    root = Tk()
    root.title("LED Status Simulator")  # GUI Title
    led_status_label = Label(root, text="", font=('Helvetica', 18))  # Initially no text
    led_status_label.pack(pady=20)
    return root, led_status_label

# Function to handle voice commands using speech recognition:
def listen_commands(led_status_label):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                control_led(command, led_status_label)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Error; {0}".format(e))
            except KeyboardInterrupt:
                print("Stopping...")
                break

# Main function setup for GUI and voice command handling:
if __name__ == "__main__":
    root, led_status_label = setup_gui()
    threading.Thread(target=lambda: listen_commands(led_status_label), daemon=True).start()
    root.mainloop()
