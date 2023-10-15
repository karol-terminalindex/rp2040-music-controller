import time
import digitalio
import board
import rotaryio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Rotary encoder
enc = rotaryio.IncrementalEncoder(board.GP13, board.GP14)
encSw = digitalio.DigitalInOut(board.GP15)
encSw.direction = digitalio.Direction.INPUT
encSw.pull = digitalio.Pull.UP
lastPosition = 0

# Media buttons
btnStop = digitalio.DigitalInOut(board.GP19)
btnStop.direction = digitalio.Direction.INPUT
btnStop.pull = digitalio.Pull.UP

btnPrev = digitalio.DigitalInOut(board.GP18)
btnPrev.direction = digitalio.Direction.INPUT
btnPrev.pull = digitalio.Pull.UP

btnPlay = digitalio.DigitalInOut(board.GP17)
btnPlay.direction = digitalio.Direction.INPUT
btnPlay.pull = digitalio.Pull.UP

btnNext = digitalio.DigitalInOut(board.GP16)
btnNext.direction = digitalio.Direction.INPUT
btnNext.pull = digitalio.Pull.UP

# builtin LED
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

# USB device
consumer = ConsumerControl(usb_hid.devices)

# button delay
dl = 0.2

# loop
while True:
    # poll encoder position
    position = enc.position
    if position != lastPosition:
        led.value = True
        if lastPosition < position:
            consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
        else:
            consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
        lastPosition = position
        led.value = False
    
    # poll encoder button
    if encSw.value == 0:
        consumer.send(ConsumerControlCode.MUTE)
        led.value = True
        time.sleep(dl)
        led.value = False
        print("Encoder button pressed")
    
    # poll media buttons
    if btnStop.value == 0:
        consumer.send(ConsumerControlCode.STOP)
        led.value = True
        time.sleep(dl)
        led.value = False
        print("Stop button pressed")
        
    if btnPrev.value == 0:
        consumer.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
        led.value = True
        time.sleep(dl)
        led.value = False
        print("Previous button pressed")
        
    if btnPlay.value == 0:
        consumer.send(ConsumerControlCode.PLAY_PAUSE)
        led.value = True
        time.sleep(dl)
        led.value = False
        print("Play/Pause button pressed")
        
    if btnNext.value == 0:
        consumer.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        led.value = True
        time.sleep(dl)
        led.value = False
        print("Next button pressed")
        
    time.sleep(0.1)
