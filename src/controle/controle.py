from machine import Pin, ADC, SPI, I2C
import time

# ========================
# CONFIG GPIO
# ========================
joy1_x = ADC(27)
joy1_y = ADC(26)
button = Pin(19, Pin.IN, Pin.PULL_UP)
led    = Pin(25, Pin.OUT)

# ========================
# I2C + DISPLAY OLED SSD1306
# ========================
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

class SSD1306:
    def __init__(self, i2c, addr=0x3C, width=128, height=64):
        self.i2c    = i2c
        self.addr   = addr
        self.width  = width
        self.height = height
        self.pages  = height // 8
        self.buffer = bytearray(self.pages * width)
        self._init_display()

    def _cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x00, cmd]))

    def _init_display(self):
        for cmd in [
            0xAE, 0x20, 0x00, 0xB0, 0xC8,
            0x00, 0x10, 0x40, 0x81, 0xFF,
            0xA1, 0xA6, 0xA8, 0x3F, 0xA4,
            0xD3, 0x00, 0xD5, 0xF0, 0xD9,
            0x22, 0xDA, 0x12, 0xDB, 0x20,
            0x8D, 0x14, 0xAF
        ]:
            self._cmd(cmd)

    def show(self):
        for page in range(self.pages):
            self._cmd(0xB0 + page)
            self._cmd(0x00)
            self._cmd(0x10)
            self.i2c.writeto(self.addr,
                bytearray([0x40]) + self.buffer[page * self.width:(page + 1) * self.width])

    def fill(self, color):
        val = 0xFF if color else 0x00
        self.buffer = bytearray([val] * len(self.buffer))

    def pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            page = y // 8
            bit  = y % 8
            idx  = page * self.width + x
            if color:
                self.buffer[idx] |= (1 << bit)
            else:
                self.buffer[idx] &= ~(1 << bit)

    FONT = {
        ' ': [0,0,0,0,0],
        'A': [0x7E,0x09,0x09,0x09,0x7E],
        'B': [0x7F,0x49,0x49,0x49,0x36],
        'C': [0x3E,0x41,0x41,0x41,0x22],
        'D': [0x7F,0x41,0x41,0x22,0x1C],
        'E': [0x7F,0x49,0x49,0x49,0x41],
        'F': [0x7F,0x09,0x09,0x09,0x01],
        'G': [0x3E,0x41,0x49,0x49,0x7A],
        'H': [0x7F,0x08,0x08,0x08,0x7F],
        'I': [0x41,0x7F,0x41,0x00,0x00],
        'J': [0x20,0x40,0x41,0x3F,0x01],
        'K': [0x7F,0x08,0x14,0x22,0x41],
        'L': [0x7F,0x40,0x40,0x40,0x40],
        'M': [0x7F,0x02,0x0C,0x02,0x7F],
        'N': [0x7F,0x04,0x08,0x10,0x7F],
        'O': [0x3E,0x41,0x41,0x41,0x3E],
        'P': [0x7F,0x09,0x09,0x09,0x06],
        'Q': [0x3E,0x41,0x51,0x21,0x5E],
        'R': [0x7F,0x09,0x19,0x29,0x46],
        'S': [0x46,0x49,0x49,0x49,0x31],
        'T': [0x01,0x01,0x7F,0x01,0x01],
        'U': [0x3F,0x40,0x40,0x40,0x3F],
        'V': [0x1F,0x20,0x40,0x20,0x1F],
        'W': [0x3F,0x40,0x38,0x40,0x3F],
        'X': [0x63,0x14,0x08,0x14,0x63],
        'Y': [0x07,0x08,0x70,0x08,0x07],
        'Z': [0x61,0x51,0x49,0x45,0x43],
        '0': [0x3E,0x51,0x49,0x45,0x3E],
        '1': [0x00,0x42,0x7F,0x40,0x00],
        '2': [0x42,0x61,0x51,0x49,0x46],
        '3': [0x21,0x41,0x45,0x4B,0x31],
        '4': [0x18,0x14,0x12,0x7F,0x10],
        '5': [0x27,0x45,0x45,0x45,0x39],
        '6': [0x3C,0x4A,0x49,0x49,0x30],
        '7': [0x01,0x71,0x09,0x05,0x03],
        '8': [0x36,0x49,0x49,0x49,0x36],
        '9': [0x06,0x49,0x49,0x29,0x1E],
        ':': [0x00,0x36,0x36,0x00,0x00],
        '-': [0x08,0x08,0x08,0x08,0x08],
        '%': [0x23,0x13,0x08,0x64,0x62],
    }

    def text(self, string, x, y, color=1):
        for ch in string.upper():
            glyph = self.FONT.get(ch, self.FONT[' '])
            for col_idx, col in enumerate(glyph):
                for row in range(8):
                    self.pixel(x + col_idx, y + row, (col >> row) & 1 if color else 0)
            x += 6
            if x > self.width:
                break

# Inicializa display
display = SSD1306(i2c)
display.fill(0)
display.text("CARRO", 30, 20)
display.text("BOMBEIRO", 16, 36)
display.show()
time.sleep(2)

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
ce  = Pin(9, Pin.OUT)

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
        self.init_tx()

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

    def init_tx(self):
        time.sleep_ms(100)
        self.write_reg(0x00, 0x0A)
        self.write_reg(0x01, 0x00)
        self.write_reg(0x02, 0x01)
        self.write_reg(0x05, 0x02)
        self.write_reg(0x06, 0x26)
        self.set_addr(0x10, ADDR_CARRO)
        self.set_addr(0x0A, ADDR_CONTROLE)
        self.write_reg(0x11, 4)
        self.flush_rx()
        self.flush_tx()
        self.write_reg(0x07, 0x70)

    def modo_rx(self):
        self.ce.value(0)
        self.write_reg(0x00, 0x0B)
        self.write_reg(0x02, 0x01)
        self.set_addr(0x0A, ADDR_CONTROLE)
        self.flush_rx()
        self.write_reg(0x07, 0x70)
        self.ce.value(1)
        time.sleep_us(150)

    def modo_tx(self):
        self.ce.value(0)
        self.write_reg(0x00, 0x0A)
        self.flush_tx()
        time.sleep_us(150)

    def send(self, data):
        self.modo_tx()
        self.csn.value(0)
        self.spi.write(bytearray([0xA0]) + data)
        self.csn.value(1)
        self.ce.value(1)
        time.sleep_us(15)
        self.ce.value(0)
        time.sleep_ms(3)
        self.write_reg(0x07, 0x70)
        self.modo_rx()

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

    def dump_regs(self):
        print("=== DUMP REGISTRADORES ===")
        print(f"CONFIG    (0x00): {self.read_reg(0x00):#04x}")
        print(f"EN_AA     (0x01): {self.read_reg(0x01):#04x}")
        print(f"EN_RXADDR (0x02): {self.read_reg(0x02):#04x}")
        print(f"RF_CH     (0x05): {self.read_reg(0x05):#04x}")
        print(f"RF_SETUP  (0x06): {self.read_reg(0x06):#04x}")
        print(f"STATUS    (0x07): {self.read_reg(0x07):#04x}")
        print(f"RX_PW_P0  (0x11): {self.read_reg(0x11):#04x}")
        self.csn.value(0)
        self.spi.write(bytearray([0x10]))
        tx_addr = self.spi.read(5)
        self.csn.value(1)
        print(f"TX_ADDR   (0x10): {[hex(b) for b in tx_addr]}")
        self.csn.value(0)
        self.spi.write(bytearray([0x0A]))
        rx0_addr = self.spi.read(5)
        self.csn.value(1)
        print(f"RX_ADDR_P0(0x0A): {[hex(b) for b in rx0_addr]}")
        print("==========================")

# ========================
# INICIALIZA RÁDIO
# ========================
radio = NRF24(spi, csn, ce)
print(">>> DUMP INICIAL (modo TX):")
radio.dump_regs()

# ========================
# FUNÇÕES
# ========================
def read_joystick(adc):
    return adc.read_u16()

def normalize(value):
    return int((value - 32768) / 32768 * 100)

# ========================
# SIMULAÇÃO DE UMIDADE
# ========================
# Velocidade de queda: quantos % por segundo segurando o botão.
# Ajuste conforme quiser — ex: 10 = cai 10% a cada segundo.
UMIDADE_QUEDA_POR_SEG = 10.0

umidade_sim       = 100       # Começa em 100% e só reseta ao religar
btn_anterior      = 1         # Estado anterior do botão (1 = solto)
btn_pressionado_t = None      # Timestamp de quando começou a pressionar

def atualizar_umidade_simulada(btn_atual):
    """
    Atualiza a umidade simulada com base no estado do botão.

    - btn_atual == 0  → botão pressionado (Pull-up ativo baixo)
    - btn_atual == 1  → botão solto

    Enquanto pressionado: diminui linearmente pelo tempo.
    Ao soltar: congela no valor atual.
    Ao pressionar de novo: continua de onde parou.
    """
    global umidade_sim, btn_anterior, btn_pressionado_t

    agora = time.ticks_ms()

    if btn_atual == 0:  # Botão pressionado
        if btn_anterior == 1:
            # Borda de descida: registra quando começou
            btn_pressionado_t = agora

        # Calcula quanto tempo está pressionado nesta sessão (ms → s)
        tempo_pressionado_s = time.ticks_diff(agora, btn_pressionado_t) / 1000.0

        # Calcula nova umidade baseada no tempo acumulado
        nova = umidade_sim - (UMIDADE_QUEDA_POR_SEG * tempo_pressionado_s)
        umidade_atual = max(0, int(nova))

    else:  # Botão solto
        if btn_anterior == 0:
            # Borda de subida: congela o valor calculado no último frame
            agora_antes = btn_pressionado_t
            tempo_s = time.ticks_diff(agora, agora_antes) / 1000.0
            nova = umidade_sim - (UMIDADE_QUEDA_POR_SEG * tempo_s)
            umidade_sim = max(0, int(nova))  # Salva o valor congelado
            btn_pressionado_t = None

        umidade_atual = umidade_sim  # Retorna o valor congelado

    btn_anterior = btn_atual
    return umidade_atual

# ========================
# LOOP PRINCIPAL
# ========================
INTERVALO_TX = 80
JANELA_RX    = 25

ultimo_tx = time.ticks_ms()

while True:

    if time.ticks_diff(time.ticks_ms(), ultimo_tx) >= INTERVALO_TX:

        x_norm = -normalize(read_joystick(joy1_x))
        y_norm = -normalize(read_joystick(joy1_y))

        btn = button.value()

        led.value(1 if btn == 0 else 0)

        # Atualiza umidade simulada
        umidade_atual = atualizar_umidade_simulada(btn)

        # Determina status (AGUA se >= 30%, SECO abaixo)
        umidade_status = "AGUA" if umidade_atual >= 30 else "SECO"

        payload = bytearray([
            x_norm & 0xFF,
            y_norm & 0xFF,
            btn,
            0
        ])

        radio.send(payload)

        ultimo_tx = time.ticks_ms()

        deadline = time.ticks_add(time.ticks_ms(), JANELA_RX)
        recebeu  = False

        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            if radio.available():
                resp = radio.receive()
                if resp[2] == 0xFF:
                    print("RX OK | Umidade real:", resp[0])
                recebeu = True
                break
            time.sleep_ms(1)

        if not recebeu:
            print(f"Sem resposta RF | Umidade SIM: {umidade_atual}% [{umidade_status}]")

        # ---- Atualiza OLED ----
        display.fill(0)

        display.text("CARRO BOMBEIRO", 4, 0)

        display.text("X:" + str(x_norm), 0, 18)
        display.text("Y:" + str(y_norm), 0, 30)

        display.text(
            "BTN:" + ("ON" if btn == 0 else "OFF"),
            0, 42
        )

        display.text(
            "UM:" + str(umidade_atual) + "% " + umidade_status,
            0, 54
        )

        display.show()

    time.sleep_ms(1)