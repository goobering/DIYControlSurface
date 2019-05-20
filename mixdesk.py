import Adafruit_GPIO.I2C as i2c
import Adafruit_GPIO.MCP230xx
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import smbus
import time
import RPi.GPIO as GPIO

# Blue / CLK: 14
# White / Dout: 15
# Yellow / Din: 18
# Grey / CS/SHD: 23

# Software SPI configuration:
CLK  = 14
MISO = 15
MOSI = 18
CS   = 23

mcp3008 = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

mcp23017 = Adafruit_GPIO.MCP230xx.MCP23017(address=0x20, busnum=1)

# Set pins to output
for i in range(0, 16):     
    mcp23017.setup(i, GPIO.OUT)

sleep_time = 0.02

pin_vals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

while(True):

    # for chan in range(0, 4):
        for i in range(0, 16):
            # print("Multiplex 1 channel %d" %i)
            pinBinary = format(i, '04b')
            # startPinObject = chan * 4
            pinObject = {8:int(pinBinary[0]), 9:int(pinBinary[1]), 10:int(pinBinary[2]), 11:int(pinBinary[3])}
            mcp23017.output_pins(pinObject)
            # time.sleep(sleep_time)
            myread = mcp3008.read_adc(0)
            if (not pin_vals[i] == int(myread)) and (int(myread) > 3):
                pin_vals[i] = myread
                print("Multiplex 0 channel %d: " %i + str(myread))
        
        # time.sleep(sleep_time)

    # for i in range(0, 16):
    #     # print("Multiplex 2 channel %d" %i)
    #     pinBinary = format(i, '04b')
    #     pinObject = {12:int(pinBinary[0]), 13:int(pinBinary[1]), 14:int(pinBinary[2]), 15:int(pinBinary[3])}
    #     mcp23017.output_pins(pinObject)
    #     time.sleep(sleep_time)
    #     myread = mcp3008.read_adc(1)
    #     print("Multiplex 2 channel %d: " %i + str(myread))
    #     time.sleep(sleep_time)