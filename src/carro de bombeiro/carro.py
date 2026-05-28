from machine import Pin, SPI, PWM, ADC
import time

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
ce  = Pin(12, Pin.OUT)

# ========================
# L298N - PONTE H
# ========================
in1 = Pin(0, Pin.OUT)
in2 = Pin(1, Pin.OUT)
ena = PWM(Pin(9))
ena.freq(1000)

in3 = Pin(2, Pin.OUT)
in4 = Pin(3, Pin.OUT)
enb = PWM(Pin(10))
enb.freq(1000)

in1.value(0)
in2.value(0)
in3.value(0)
in4.value(0)
ena.duty_u16(0)
enb.duty_u16(0)

# ========================
# BOMBA D'ÁGUA - GP8
# ========================
bomba = Pin(8, Pin.OUT)
bomba.value(0)

# LED indicador
led = Pin(13, Pin.OUT)

# ========================
# SENSOR DE UMIDADE
# ========================
umidade_analog  = ADC(Pin(27))
umidade_digital = Pin(22, Pin.IN)

FORA     = 60000
SUBMERSO = 10000

def ler_umidade():
    raw = sum(umidade_analog.read_u16() for _ in range(10)) // 10
    nivel = (FORA - raw) * 100 // (FORA - SUBMERSO)
    nivel = max(0, min(100, nivel))
    digital = 1 if umidade_digital.value() == 0 else 0
    return nivel, digital

# ========================
# ENDEREÇOS
# ========================
ADDR_CONTROLE = [0xE7,0xE7,0xE7,0xE7,0xE7]
ADDR_CARRO    = [0xC2,0xC2,0xC2,0xC2,0xC2]

# ========================
# DRIVER NRF24L01
# ========================
class NRF24:
    def __init__(self, spi, csn, ce):
        self.spi = spi
        self.csn = csn
        self.ce  = ce
        self.csn.value(1)
        self.ce.value(0)
        self.init_rx()

    def write_reg(self, reg, value):
        self.csn.value(0)
        self.spi.write(bytearray([0x20 | reg, value]))
        self.csn.value(1)

    def read_reg(self, reg):
        self.csn.value(0)
        self.spi.write(bytearray([reg & 0x1F]))
        result = self.spi.read(1)
        self.csn.value(1)
        return result[0]

    def set_addr(self, pipe_reg, addr_bytes):
        self.csn.value(0)
        self.spi.write(bytearray([0x20 | pipe_reg]) + bytearray(addr_bytes))
        self.csn.value(1)

    def flush_rx(self):
        self.csn.value(0)
        self.spi.write(bytearray([0xE2]))
        self.csn.value(1)

    def flush_tx(self):
        self.csn.value(0)
        self.spi.write(bytearray([0xE1]))
        self.csn.value(1)

    def init_rx(self):
        time.sleep_ms(100)
        self.write_reg(0x00, 0x0B)   # Power up + RX
        self.write_reg(0x01, 0x00)   # Sem auto-ack
        self.write_reg(0x02, 0x01)   # Pipe 0 habilitado
        self.write_reg(0x05, 0x02)   # Canal 2
        self.write_reg(0x06, 0x26)   # Data rate 1Mbps

        self.set_addr(0x0A, ADDR_CARRO)  # RX pipe 0 addr
        self.set_addr(0x10, ADDR_CONTROLE)  # TX addr (resposta)
        self.write_reg(0x11, 4)             # Payload pipe 0 = 4 bytes

        self.flush_rx()
        self.flush_tx()
        self.write_reg(0x07, 0x70)
        self.ce.value(1)

    def modo_tx(self):
        self.ce.value(0)
        self.write_reg(0x00, 0x0A)
        self.set_addr(0x10, ADDR_CONTROLE)  # TX aponta para o controle
        self.flush_tx()
        time.sleep_us(150)

    def modo_rx(self):
        self.ce.value(0)
        self.write_reg(0x00, 0x0B)
        self.set_addr(0x0A, ADDR_CARRO)
        self.flush_rx()
        self.write_reg(0x07, 0x70)
        self.ce.value(1)
        time.sleep_us(150)

    def available(self):
        status = self.read_reg(0x07)
        if status & 0x10:
            self.write_reg(0x07, 0x70)
            self.flush_rx()
        return (status & 0x40) != 0

    def receive(self):
        self.csn.value(0)
        self.spi.write(bytearray([0x61]))
        data = self.spi.read(4)
        self.csn.value(1)
        self.write_reg(0x07, 0x40)
        return data

    def send(self, data):
        self.modo_tx()
        self.csn.value(0)
        self.spi.write(bytearray([0xA0]) + data)
        self.csn.value(1)
        self.ce.value(1)
        time.sleep_us(20)
        self.ce.value(0)
        time.sleep_ms(5)
        self.write_reg(0x07, 0x70)
        self.modo_rx()

    def reset(self):
        self.ce.value(0)
        self.flush_rx()
        self.flush_tx()
        self.write_reg(0x07, 0x70)
        self.modo_rx()
        print("Radio reiniciado!")

# ========================
# FUNÇÕES DOS MOTORES
# ========================
def set_motor(in_a, in_b, en_pwm, speed):
    speed = max(-100, min(100, speed))
    if speed >= 10:
        in_a.value(1)
        in_b.value(0)
        en_pwm.duty_u16(int(speed / 100 * 65535))
    elif speed <= -10:
        in_a.value(0)
        in_b.value(1)
        en_pwm.duty_u16(int(abs(speed) / 100 * 65535))
    else:
        in_a.value(0)
        in_b.value(0)
        en_pwm.duty_u16(0)

def drive(x, y):
    motor_esq = max(-100, min(100, y + x))
    motor_dir = max(-100, min(100, y - x))
    set_motor(in1, in2, ena, motor_esq)
    set_motor(in3, in4, enb, motor_dir)

def parar():
    set_motor(in1, in2, ena, 0)
    set_motor(in3, in4, enb, 0)

# ========================
# INICIALIZA RÁDIO
# ========================
radio = NRF24(spi, csn, ce)
print("Receptor pronto, aguardando sinal...")
radio.modo_rx()  # Garantir RX mode ao iniciar

# Debug: mostrar config inicial
print(">>> CONFIG INICIAL (RX):")
print(f"CONFIG: {radio.read_reg(0x00):#04x} | EN_RX: {radio.read_reg(0x02):#04x} | CH: {radio.read_reg(0x05):#04x}")

# ========================
# LOOP PRINCIPAL
# ========================
TIMEOUT       = 500
TIMEOUT_RESET = 2000

ultimo_sinal  = time.ticks_ms()
primeiro_dump = True

while True:
    if radio.available():
        data = radio.receive()
        t0 = time.ticks_ms()

        y   = data[0] if data[0] < 128 else data[0] - 256
        x   = data[1] if data[1] < 128 else data[1] - 256
        btn = data[2]

        drive(x, y)
        bomba.value(1 if btn == 0 else 0)
        led.value(1)
        ultimo_sinal = time.ticks_ms()

        umid_pct, umid_dig = ler_umidade()
        t1 = time.ticks_ms()

        payload_umid = bytearray([
            umid_pct & 0xFF,
            umid_dig & 0xFF,
            0xFF,
            0
        ])

        radio.send(payload_umid)
        time.sleep_ms(50)  # Aumentado de 15ms → 50ms para garantir que resposta chega ao controle
        radio.modo_rx()    # Voltar para RX mode
        t2 = time.ticks_ms()

        print(f"X: {x} | Y: {y} | BOMBA: {1 if btn == 0 else 0} | "
              f"Nivel: {umid_pct}% | {'AGUA' if umid_dig == 1 else 'SECO'}")
        print(f"RESPOSTA_TX | Umidade: {umid_pct}% | Tempo ate envio: {time.ticks_diff(t1, t0)}ms | Total: {time.ticks_diff(t2, t0)}ms")

    if time.ticks_diff(time.ticks_ms(), ultimo_sinal) > TIMEOUT:
        parar()
        bomba.value(0)
        led.value(0)

    if time.ticks_diff(time.ticks_ms(), ultimo_sinal) > TIMEOUT_RESET:
        radio.reset()
        ultimo_sinal = time.ticks_ms()

    time.sleep_ms(10)