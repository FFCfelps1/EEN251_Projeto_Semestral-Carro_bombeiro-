# Diagrama de Blocos — Carro Bombeiro Teleoprado

> Representação detalhada em formato texto e Mermaid do sistema completo.  
> Para renderização visual, abra este arquivo em um visualizador Mermaid (GitHub, VSCode com extensão, Obsidian, etc.)

---

## 1. Diagrama de Blocos Principal (Sistema Completo)

```
╔══════════════════════════════════════════════════════════╗
║              BLOCO TRANSMISSOR (Controle Remoto)         ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   ┌──────────────┐       ┌───────────────────────────┐   ║
║   │ Bateria LiPo │──────▶│  Raspberry Pi Pico (TX)   │   ║
║   │    3,7 V     │       │                           │   ║
║   └──────────────┘       │  ADC0 ◀── Joystick Eixo X │   ║
║                          │  ADC1 ◀── Joystick Eixo Y │   ║
║   ┌──────────────┐       │  GP19 ◀── Botão Bomba     │   ║
║   │ OLED SSD1306 │◀─────▶│  I2C0 ──▶ Display Status  │   ║
║   └──────────────┘       │  SPI0 ──▶ NRF24L01 (TX)   │   ║
║                          └───────────────────────────┘   ║
║                                        │                 ║
║                              NRF24L01 ─┘                 ║
╚══════════════════════════════════════╪═══════════════════╝
                                       │
                               RF 2,4 GHz
                           Enhanced ShockBurst
                                       │
╔══════════════════════════════════════╪═══════════════════╗
║              BLOCO RECEPTOR (Carro Bombeiro)             ║
╠══════════════════════════════════════╪═══════════════════╣
║                              NRF24L01 (RX)               ║
║                                       │ SPI0             ║
║   ┌───────────────┐       ┌───────────▼───────────────┐  ║
║   │  Bateria 2S   │──────▶│  Raspberry Pi Pico (RX)   │  ║
║   │   7,4 V       │       │                           │  ║
║   └───┬───────────┘       │  GP0, 1 ──▶ IN1, IN2 (Mot)│  ║
║       │                   │  GP2, 3 ──▶ IN3, IN4 (Mot)│  ║
║       ▼                   │  GP9, 10──▶ ENA, ENB (PWM)│  ║
║  ┌──────────────┐          │  GP8     ──▶ Relé Bomba   │  ║
║  │ Regulador   │          │  GP27 ADC ◀── Sensor Nív. │  ║
║  │ 7,4V → 5V  │          │  GP22     ◀── Sensor (D)   │  ║
║  └──────┬───────┘          │  GP13     ──▶ LED Status  │  ║
║         │                  └───────────────────────────┘  ║
║         │                                                  ║
║         ├──────────────────────────────────────────────┐  ║
║         │                                              │  ║
║         ▼                    ▼                         ▼  ║
║   ┌──────────┐        ┌───────────┐            ┌──────────┐║
║   │ Driver   │        │   Relé    │            │  Bomba   │║
║   │  L298N   │        │    5V     │            │ d'água   │║
║   └──┬────┬──┘        └─────┬─────┘            └─────┬────┘║
║      │    │                 │                        │     ║
║      ▼    ▼                 ▼                        ▼     ║
║   Motores Esq        Motores Dir               Jato d'água ║
║   (4WD)              (4WD)                                 ║
║                                                            ║
║                                             ┌─────▼────┐  ║
║                          Sensor Nível ◀─────│Reservat. │  ║
║                                             └──────────┘  ║
╚══════════════════════════════════════════════════════════╝
```

---

## 2. Diagrama Mermaid — Subsistema Transmissor

```mermaid
graph TD
    BAT_TX["🔋 Bateria LiPo\n3,7V"]
    PICO_TX["⚙️ Raspberry Pi Pico TX\n(RP2040)"]
    JOY_X["🕹️ Joystick — Eixo X\n(ADC0 / GP27)"]
    JOY_Y["🕹️ Joystick — Eixo Y\n(ADC1 / GP26)"]
    BTN1["🔴 Botão Bomba\n(GP19 — pull-up)"]
    OLED["🖥️ Display OLED\n(I2C0 / GP0, 1)"]
    NRF_TX["📡 NRF24L01\n(SPI0 | PTX mode)"]
    RF["≋≋≋ RF 2,4 GHz ≋≋≋\nEnhanced ShockBurst"]

    BAT_TX -->|"3,3V (via Pico onboard)"| PICO_TX
    JOY_X -->|"ADC 0–3,3V"| PICO_TX
    JOY_Y -->|"ADC 0–3,3V"| PICO_TX
    BTN1 -->|"GPIO LOW = pressionado"| PICO_TX
    PICO_TX -->|"I2C SDA/SCL"| OLED
    PICO_TX -->|"SPI: SCK/MOSI/MISO/CS/CE"| NRF_TX
    NRF_TX -->|"Pacote 4 bytes @ ~12Hz"| RF
```

---

## 3. Diagrama Mermaid — Subsistema Receptor

```mermaid
graph TD
    BAT_RX["🔋 Bateria 2S\n7,4V / 2000mAh"]
    REG["⚡ Regulador DC-DC\n7,4V → 5V (MP1584)"]
    PICO_RX["⚙️ Raspberry Pi Pico RX\n(RP2040)"]
    RF_IN["≋≋≋ RF 2,4 GHz ≋≋≋"]
    NRF_RX["📡 NRF24L01\n(SPI0 | PRX mode)"]
    L298N["🔧 Driver L298N\n(Motores)"]
    M1["⚙ Motor Esq.\nDiant + Tras"]
    M2["⚙ Motor Dir.\nDiant + Tras"]
    RELAY["🔌 Relé 5V\n(Bomba)"]
    PUMP["💧 Mini Bomba d'água\n3–6V DC"]
    SENSOR_A["📊 Sensor Nível (A)\nADC / GP27"]
    SENSOR_D["🚨 Alerta Nível (D)\nGPIO / GP22"]
    LED["💡 LED Indicador\nStatus RF / GP13"]

    BAT_RX -->|"7,4V"| REG
    REG -->|"5V"| L298N
    REG -->|"5V"| RELAY
    REG -->|"3,3V via Pico VSYS"| PICO_RX

    RF_IN -->|"pacote recebido"| NRF_RX
    NRF_RX -->|"SPI: interrupção IRQ"| PICO_RX

    PICO_RX -->|"PWM ENA/ENB + IN1–IN4"| L298N
    L298N --> M1
    L298N --> M2

    PICO_RX -->|"GPIO OUT / GP8"| RELAY
    RELAY -->|"5V chaveado"| PUMP
    
    SENSOR_A -->|"analog"| PICO_RX
    SENSOR_D -->|"digital"| PICO_RX
    PICO_RX -->|"GPIO OUT"| LED
```

---

## 4. Diagrama de Estados — Receptor (Firmware)

```mermaid
stateDiagram-v2
    [*] --> INICIALIZANDO

    INICIALIZANDO --> AGUARDANDO_RF : configuração concluída

    AGUARDANDO_RF --> RECEBENDO_PACOTE : IRQ NRF24L01
    AGUARDANDO_RF --> FAILSAFE : timeout > 500ms

    RECEBENDO_PACOTE --> STOP : stop == 1
    RECEBENDO_PACOTE --> MOVENDO : stop == 0

    MOVENDO --> BOMBA_ON : bomba == 1
    MOVENDO --> BOMBA_OFF : bomba == 0
    BOMBA_ON --> AGUARDANDO_RF
    BOMBA_OFF --> AGUARDANDO_RF

    STOP --> AGUARDANDO_RF

    FAILSAFE --> AGUARDANDO_RF : pacote válido recebido

    note right of FAILSAFE
        Todos os motores parados
        Bomba desligada
        LED piscando
    end note

    note right of MOVENDO
        PWM aplicado nos L298N
        Velocidade diferencial
        por lado (tank drive)
    end note
```

---

## 5. Estrutura do Pacote RF

```
┌─────────┬──────────────────────────────────────────────────┐
│  Byte   │  Descrição                                        │
├─────────┼──────────────────────────────────────────────────┤
│    0    │  vel_esq  — int8  — velocidade lado esq. (−100..+100) │
│    1    │  vel_dir  — int8  — velocidade lado dir. (−100..+100) │
│    2    │  bomba    — uint8 — 0=OFF, 1=ON                   │
│    3    │  stop     — uint8 — 0=normal, 1=parada emergência │
└─────────┴──────────────────────────────────────────────────┘
Tamanho total: 4 bytes (campo fixo — NRF24L01 static payload)
Taxa: ~12 pacotes/segundo (conforme configurado no firmware)
```

---

## 6. Diagrama de Alimentação

```
Bateria 2S (7,4V)
       │
       ├──[Regulador DC-DC MP1584]──→ 5V ──┬── L298N (VCC lógico)
       │                                   ├── Relé 5V (bobina)
       │                                   └── Pico (VSYS → regulador 3,3V interno)
       │                                            │
       │                                           3,3V ──── NRF24L01 VCC
       │
       └──[Direto 7,4V]──→ L298N (pino VS — potência dos motores)
                           (corrente pico ~2A por driver, 4A total)
```

---

*Arquivo gerado em 11 de março de 2026 — EEN251 Projeto Semestral.*
