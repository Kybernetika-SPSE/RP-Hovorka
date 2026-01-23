"""Python code for interfacing with Canon EF lens using ESP32"""
# ESP32 MicroPython Communication with Canon EF Lens

"""
This script allows the ESP32 to communicate with a Canon EF lens using MicroPython.
It handles initialization, focusing, and zoom control to integrate with various camera systems.
"""

from machine import Pin, UART
import time

class CanonEFLens:
    def __init__(self, uart_tx, uart_rx, baud_rate=9600):
        self.uart = UART(1, baudrate=baud_rate, tx=Pin(uart_tx), rx=Pin(uart_rx))
        time.sleep(2)  # Allow some time for connection

    def send_command(self, command):
        self.uart.write(command)
        time.sleep(0.1)  # Wait for the lens to process command

    def focus(self):
        self.send_command(b'FOCUS')  # Replace with actual command for focusing

    def zoom(self, level):
        self.send_command(f'ZOOM {level}'.encode())  # Replace with actual command for zoom

    def stop(self):
        self.send_command(b'STOP')  # Replace with actual command to stop lens

# Example usage:
if __name__ == '__main__':
    lens = CanonEFLens(uart_tx=17, uart_rx=16)
    lens.focus()
    lens.zoom(75)
    lens.stop()