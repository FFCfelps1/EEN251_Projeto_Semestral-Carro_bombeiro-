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
║                          │  GP14 ◀── Botão Bomba     │   ║
║                          │  GP15 ◀── Botão Stop      │   ║
║                          │  SPI0 ──▶ NRF24L01 (TX)   │   ║
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
║   └───┬───────────┘       │  GP8  PWM ──▶ L298N #1    │  ║
║       │                   │  GP9  PWM ──▶ L298N #1    │  ║
║       ▼                   │  GP10–13 ──▶ L298N #1     │  ║
║  ┌──────────────┐          │  GP16 PWM ──▶ L298N #2    │  ║
║  │ Regulador   │          │  GP17 PWM ──▶ L298N #2    │  ║
║  │ 7,4V → 5V  │          │  GP18–21 ──▶ L298N #2     │  ║
║  └──────┬───────┘          │  GP22     ──▶ Relé 5V     │  ║
║         │                  │  GP26 ADC ◀── Sensor Nív. │  ║
║         │                  │  GP27     ──▶ LED Alerta  │  ║
║         │                  │  GP28     ──▶ Buzzer      │  ║
║         │                  └───────────────────────────┘  ║
║         │                                                  ║
║         ├──────────────────────────────────────────────┐  ║
║         │                                              │  ║
║         ▼                    ▼                         ▼  ║
║   ┌──────────┐        ┌───────────┐            ┌──────────┐║
║   │ L298N #1 │        │ L298N #2  │            │  Relé 5V ││
║   │          │        │           │            └──────────┘║
║   └──┬────┬──┘        └──┬─────┬──┘                 │     ║
║      │    │              │     │                    ▼     ║
║      ▼    ▼              ▼     ▼             ┌──────────┐  ║
║   Motor1 Motor2       Motor3 Motor4          │  Bomba   │  ║
║   (D.Esq)(T.Esq)     (D.Dir)(T.Dir)         │ d'água   │  ║
║                                             └─────┬────┘  ║
║                                                   │       ║
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
    JOY_X["🕹️ Joystick — Eixo X\n(ADC0 / GP26)"]
    JOY_Y["🕹️ Joystick — Eixo Y\n(ADC1 / GP27)"]
    BTN1["🔴 Botão Bomba\n(GP14 — pull-up)"]
    BTN2["⛔ Botão Stop/Emergência\n(GP15 — pull-up)"]
    NRF_TX["📡 NRF24L01\n(SPI0 | PTX mode)"]
    RF["≋≋≋ RF 2,4 GHz ≋≋≋\nEnhanced ShockBurst"]

    BAT_TX -->|"3,3V (via Pico onboard)"| PICO_TX
    JOY_X -->|"ADC 0–3,3V"| PICO_TX
    JOY_Y -->|"ADC 0–3,3V"| PICO_TX
    BTN1 -->|"GPIO LOW = pressionado"| PICO_TX
    BTN2 -->|"GPIO LOW = pressionado"| PICO_TX
    PICO_TX -->|"SPI: SCK/MOSI/MISO/CS/CE"| NRF_TX
    NRF_TX -->|"Pacote 6 bytes @ ~50Hz"| RF
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
    L298N_A["🔧 L298N #1\n(Lado Esquerdo)"]
    L298N_B["🔧 L298N #2\n(Lado Direito)"]
    M1["⚙ Motor 1\nDianteiro Esq."]
    M2["⚙ Motor 2\nTraseiro Esq."]
    M3["⚙ Motor 3\nDianteiro Dir."]
    M4["⚙ Motor 4\nTraseiro Dir."]
    RELAY["🔌 Relé 5V\n(1 canal)"]
    PUMP["💧 Mini Bomba d'água\n3–6V DC"]
    RESERV["🪣 Reservatório\n~150 mL"]
    SENSOR["📊 Sensor de Nível\n(ADC / GP26)"]
    LED["💡 LED Vermelho\nAlerta Nível Baixo"]
    BUZZ["🔊 Buzzer\nAlerta Sonoro"]

    BAT_RX -->|"7,4V"| REG
    REG -->|"5V"| L298N_A
    REG -->|"5V"| L298N_B
    REG -->|"5V"| RELAY
    REG -->|"3,3V via Pico VSYS"| PICO_RX

    RF_IN -->|"pacote recebido"| NRF_RX
    NRF_RX -->|"SPI: interrupção IRQ"| PICO_RX

    PICO_RX -->|"PWM ENA/ENB + IN1–IN4"| L298N_A
    PICO_RX -->|"PWM ENA/ENB + IN1–IN4"| L298N_B
    L298N_A --> M1
    L298N_A --> M2
    L298N_B --> M3
    L298N_B --> M4

    PICO_RX -->|"GPIO HIGH/LOW"| RELAY
    RELAY -->|"5V chaveado"| PUMP
    PUMP -->|"pressuriza"| RESERV
    RESERV -->|"contato elétrico"| SENSOR
    SENSOR -->|"tensão analógica"| PICO_RX

    PICO_RX -->|"GPIO OUT"| LED
    PICO_RX -->|"GPIO OUT"| BUZZ
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
│    4    │  reservado                                        │
│    5    │  reservado                                        │
└─────────┴──────────────────────────────────────────────────┘
Tamanho total: 6 bytes (campo fixo — NRF24L01 static payload)
Taxa: ~50 pacotes/segundo (período de 20 ms no TX)
```

---

## 6. Diagrama de Alimentação

```
Bateria 2S (7,4V)
       │
       ├──[Regulador DC-DC MP1584]──→ 5V ──┬── L298N #1 (VCC lógico)
       │                                   ├── L298N #2 (VCC lógico)
       │                                   ├── Relé 5V (bobina)
       │                                   └── Pico (VSYS → regulador 3,3V interno)
       │                                            │
       │                                           3,3V ──── NRF24L01 VCC
       │
       └──[Direto 7,4V]──→ L298N #1 e #2 (pino VS — potência dos motores)
                           (corrente pico ~2A por driver, 4A total)
```

---

*Arquivo gerado em 11 de março de 2026 — EEN251 Projeto Semestral.*
