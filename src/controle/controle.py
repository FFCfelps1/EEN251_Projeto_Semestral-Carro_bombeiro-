from machine import Pin, ADC, SPI
import time

# ========================
# CONFIG GPIO
# ========================
# Joysticks
joy1_x = ADC(26)  # ADC0 (GPIO26)
joy1_y = ADC(27)  # ADC1 (GPIO27)

# Botão CLICÁVEL do joystick (pino SW)
button = Pin(19, Pin.IN, Pin.PULL_UP)  # ← GPIO19

# LED onboard do Pico (GPIO25)
led = Pin(25, Pin.OUT)  # ← era GPIO17, agora LED da placa

# ========================
# SPI NRF24L01
# ========================
spi = SPI(0,
          baudrate=1000000,
          polarity=0,
          phase=0,
          sck=Pin(6),
          mosi=Pin(7),
          miso=Pin(4))
csn = Pin(5, Pin.OUT)
ce = Pin(9, Pin.OUT)

# ========================
# DRIVER SIMPLES NRF24L01
# ========================
class NRF24:
    def __init__(self, spi, csn, ce):
        self.spi = spi
        self.csn = csn
        self.ce = ce
        self.csn.value(1)
        self.ce.value(0)
        self.init()

    def write_reg(self, reg, value):
        self.csn.value(0)
        self.spi.write(bytearray([0x20 | reg, value]))
        self.csn.value(1)

    def init(self):
        self.write_reg(0x00, 0x0A)  # Power up + TX mode
        self.write_reg(0x01, 0x00)  # No auto ack
        self.write_reg(0x05, 0x02)  # Canal
        self.write_reg(0x06, 0x06)  # Data rate

    def send(self, data):
        self.csn.value(0)
        self.spi.write(bytearray([0xA0]) + data)
        self.csn.value(1)
        self.ce.value(1)
        time.sleep_us(15)
        self.ce.value(0)

# Inicializa rádio
radio = NRF24(spi, csn, ce)

# ========================
# FUNÇÕES
# ========================
def read_joystick(adc):
    return adc.read_u16()

def normalize(value):
    return int((value - 32768) / 32768 * 100)

# ========================
# LOOP PRINCIPAL
# ========================
while True:
    x = read_joystick(joy1_x)
    y = read_joystick(joy1_y)

    x_norm = -normalize(x)
    y_norm = -normalize(y)

    btn = button.value()  # 0 = pressionado

    # LED onboard acende ao clicar o joystick
    led.value(1 if btn == 0 else 0)

    # Monta pacote (4 bytes)
    payload = bytearray([
        x_norm & 0xFF,
        y_norm & 0xFF,
        btn,
        0  # reservado
    ])

    radio.send(payload)

    print("X:", x_norm, "Y:", y_norm, "BTN:", 1 if btn == 0 else 0)

    time.sleep(0.1)