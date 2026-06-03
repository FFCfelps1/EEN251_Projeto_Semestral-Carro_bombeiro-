# 🚒 EEN251 — Carro de Bombeiro Teleoprado

> **Disciplina:** EEN251 — Projeto Integrador de Sistemas Embarcados  
> **Semestre:** 1º Semestre / 2026  
> **Data de início:** Março de 2026

---

## Sumário

1. [Integrantes e Responsabilidades](#1-integrantes-e-responsabilidades)
2. [Descrição Geral do Projeto](#2-descrição-geral-do-projeto)
3. [Objetivos](#3-objetivos)
4. [Estrutura do Repositório](#4-estrutura-do-repositório)
5. [Materiais e Componentes](#5-materiais-e-componentes)
6. [Arquitetura do Sistema](#6-arquitetura-do-sistema)
7. [Pinagem e Conexões](#7-pinagem-e-conexões)
8. [Firmware — Descrição e Fluxograma de Estados](#8-firmware--descrição-e-fluxograma-de-estados)
9. [Convenção de Commits](#9-convenção-de-commits)
10. [Política de Tags e Versões](#10-política-de-tags-e-versões)
11. [Cronograma](#11-cronograma)
12. [Orçamento Total Estimado](#12-orçamento-total-estimado)
13. [Referências Bibliográficas](#13-referências-bibliográficas)

---

## 1. Integrantes e Responsabilidades

| Nome | RA | Função Principal |
|------|----|-----------------|
| Felipe Fazio da Costa | 23.00055-4 | Firmware do Receptor (Pico RX) — motores e bomba |
| João Gabriel Fioruci Roberto | 23.00617-0 | Firmware do Transmissor (Pico TX) — controle RF |
| Gabriel Rodrigues Marques | 23.00578-5 | Hardware — montagem do chassi e fiação |
| Fábio Sadao Sato | 22.00984-0 | Integração do sistema e documentação |

---

## Resumo

Este relatório descreve o desenvolvimento de um protótipo de carro de bombeiro teleoprado utilizando microcontroladores Raspberry Pi Pico e comunicação via rádio frequência (NRF24L01). O sistema integra tração 4WD, sistema de combate a incêndio por bomba d'água e monitoramento de nível de reservatório. Foram aplicados conceitos de sistemas embarcados, comunicação sem fio e controle de periféricos via PWM. Os resultados demonstram a eficácia da plataforma RP2040 em aplicações de controle em tempo real e teleoperação robusta.

**Palavras-chave**: Raspberry Pi Pico. NRF24L01. MicroPython. Carro de Bombeiro. Sistemas Embarcados.

## Abstract

This report describes the development of a teleoperated fire truck prototype using Raspberry Pi Pico microcontrollers and radio frequency communication (NRF24L01). The system integrates 4WD traction, a water pump fire suppression system, and reservoir level monitoring. Concepts of embedded systems, wireless communication, and peripheral control via PWM were applied. The results demonstrate the effectiveness of the RP2040 platform in real-time control applications and robust teleoperation.

**Keywords**: Raspberry Pi Pico. NRF24L01. MicroPython. Fire Truck. Embedded Systems.

---

## 2. Descrição Geral do Projeto

O projeto consiste no desenvolvimento de um veículo robótico em escala inspirado em um caminhão de bombeiro, capaz de se locomover de maneira teleoprada por meio de comunicação sem fio RF 2.4 GHz (módulo NRF24L01). O veículo é dotado de tração 4WD com quatro motores DC controlados por dois módulos L298N, uma mini bomba d'água acionável remotamente, e um reservatório de água com sensor de nível que alerta o operador quando a água estiver baixa.

O sistema é dividido em dois blocos principais:

- **Transmissor (controle remoto):** baseado em um Raspberry Pi Pico com joystick analógico, botões e display OLED SSD1306, responsável por capturar os comandos do operador e enviá-los via NRF24L01.
- **Receptor (carro):** baseado em um segundo Raspberry Pi Pico que recebe os pacotes RF, interpreta os comandos e aciona os motores, a bomba e os alertas de nível.

Todo o firmware é desenvolvido em **MicroPython**, aproveitando a plataforma Raspberry Pi Pico (microcontrolador RP2040).

---

## 3. Objetivos

O objetivo geral deste trabalho é projetar e construir um veículo robótico controlado remotamente via radiofrequência, capaz de realizar manobras de locomoção e acionamento de uma bomba d'água, com monitoramento de status em tempo real.

### 3.1 Objetivos Específicos

- Implementação de comunicação bidirecional robusta entre controle e veículo;
- Controle de tração diferencial (tank drive) para quatro motores;
- Sistema de alerta de nível de água com indicadores visuais e sonoros;
- Desenvolvimento de firmware em MicroPython para a plataforma Raspberry Pi Pico.

---

## 4. Estrutura do Repositório

```
EEN251_Projeto_Semestral(Carro_bombeiro)/
│
├── docs/                        # Documentação HTML do projeto
│   ├── index.html               # Página principal (abas: Requisitos + Diagramas)
│   ├── diagrama_blocos.html     # Diagrama de blocos standalone (legado)
│   └── diagrama_blocos.md       # Diagrama de blocos em Markdown
│
├── firmware/                    # Código MicroPython (a ser criado)
│   ├── tx/                      # Firmware do transmissor (Pico TX)
│   │   └── main.py
│   └── rx/                      # Firmware do receptor (Pico RX)
│       └── main.py
│
├── hardware/                    # Arquivos de hardware (a ser criado)
│   ├── esquematico.pdf
│   └── lista_materiais.csv
│
├── index.html                   # Redirecionamento para docs/index.html
└── README.md                    # Este arquivo
```

---

## 5. Materiais e Componentes

| Qtd | Componente | Finalidade | Preço Est. (R$) |
|-----|-----------|-----------|:--------------:|
| 2 | Raspberry Pi Pico (RP2040) | Controlador central — TX e RX | 35,00 cada |
| 4 | Motor DC 3–6 V com caixa de redução (TT Motor) | Tração 4WD do veículo | 8,00 cada |
| 2 | Módulo L298N (ponte H dupla) | Driver de corrente para os motores | 15,00 cada |
| 2 | Módulo NRF24L01 (PA+LNA opcional) | Comunicação RF 2.4 GHz | 12,00 cada |
| 1 | Mini bomba d'água submersa 3–6 V | Jato d'água do caminhão | 18,00 |
| 1 | Módulo relé 5 V (1 canal) | Chaveamento de corrente da bomba | 6,00 |
| 1 | Sensor de nível d'água (resistivo/capacitivo) | Monitorar volume no reservatório | 5,00 |
| 1 | Chassi 4WD em acrílico ou MDF | Estrutura física do veículo | 45,00 |
| 1 | Bateria LiPo 3,7 V 1000 mAh (18650) | Alimentação do transmissor | 25,00 |
| 1 | Pack 2S 18650 (7,4 V ~2000 mAh) | Alimentação principal do carro | 40,00 |
| 1 | Módulo redutor DC-DC (MP1584 ou LM2596) | Regular 7,4 V → 5 V | 8,00 |
| 1 | Joystick analógico duplo eixo (KY-023) | Controle direcional (X/Y) | 12,00 |
| 2 | Push button (6 mm) | Ativar bomba / parada de emergência | 1,00 cada |
| 1 | Reservatório plástico (~100–200 mL) | Tanque de água do caminhão | 10,00 |
| 1 | Protoboard ou PCB de prototipagem | Prototipagem do circuito | 15,00 |
| — | Jumpers, fios, resistores, LEDs, buzzer, suportes | Conexões e indicadores | 20,00 |

**Total estimado: R$ 362,00**

---

## 6. Arquitetura do Sistema

```
[Joystick X/Y + Botões]
        │
        ▼
  Pico TX — leitura ADC/GPIO (~20 ms)
        │
        ▼
  Monta pacote: { vel_esq, vel_dir, bomba, stop }  (6 bytes)
        │
        ▼
  NRF24L01 TX ──[ RF 2,4 GHz · Enhanced ShockBurst ]──▶ NRF24L01 RX
                                                               │
                                               Pico RX — decodifica pacote
                                                               │
                              ┌────────────────┬──────────────┘
                              ▼                ▼              ▼
                       L298N #1           L298N #2        GPIO Relé
                    (Motor 1 e 2)       (Motor 3 e 4)     (Bomba)
```

**Mapeamento Tank Drive:**
```
vel_esq = Y + X
vel_dir = Y − X
```
Onde Y = eixo vertical (avanço/recuo) e X = eixo horizontal (giro). Valores limitados a [−100, +100].

---

## 7. Pinagem e Conexões

### Receptor — Raspberry Pi Pico (RX)

| Pino | GPIO | Periférico | Sinal | Obs. |
|------|:----:|-----------|-------|------|
| GP0 | 0 | L298N | IN1 | Direção Motor Esq |
| GP1 | 1 | L298N | IN2 | Direção Motor Esq |
| GP2 | 2 | L298N | IN3 | Direção Motor Dir |
| GP3 | 3 | L298N | IN4 | Direção Motor Dir |
| GP4 | 4 | NRF24L01 | MISO (SPI0) | Dados entrada |
| GP5 | 7 | NRF24L01 | CSn | Chip Select |
| GP6 | 4 | NRF24L01 | SCK (SPI0) | Clock SPI |
| GP7 | 11 | NRF24L01 | MOSI (SPI0) | Dados saída |
| GP8 | 29 | Relé Bomba | Sinal | Ativa bomba |
| GP9 | 11 | L298N | ENA (PWM) | Vel. Motor Esq |
| GP10 | 12 | L298N | ENB (PWM) | Vel. Motor Dir |
| GP12 | 6 | NRF24L01 | CE | Chip Enable |
| GP13 | 32 | LED Indicador | GPIO OUT | Status sinal |
| GP22 | 34 | Sensor Nível (D) | GPIO IN | Alerta digital |
| GP27 | 31 | Sensor Nível (A) | ADC1 | Leitura analógica |

### Transmissor — Raspberry Pi Pico (TX)

| Pino | GPIO | Periférico | Sinal | Obs. |
|------|:----:|-----------|-------|------|
| GP0 | 0 | Display OLED | I2C SDA | Dados I2C |
| GP1 | 1 | Display OLED | I2C SCL | Clock I2C |
| GP4 | 6 | NRF24L01 | MISO (SPI0) | Dados entrada |
| GP5 | 7 | NRF24L01 | CSn | Chip Select |
| GP6 | 4 | NRF24L01 | SCK (SPI0) | Clock SPI |
| GP7 | 5 | NRF24L01 | MOSI (SPI0) | Dados saída |
| GP9 | 9 | NRF24L01 | CE | Chip Enable |
| GP19 | 19 | Botão Bomba | GPIO IN | Pull-up interno |
| GP26 | 32 | Joystick Y | ADC1 | Eixo vertical |
| GP27 | 31 | Joystick X | ADC0 | Eixo horizontal |

> ⚠️ **Atenção:** O NRF24L01 opera em **3,3 V**. Nunca conecte o VCC ao pino 5V.

---

## 8. Firmware — Descrição e Fluxograma de Estados

### Transmissor (Pico TX) — loop de ~20 ms
1. Lê ADC do joystick (0–65535) → mapeia para −100…+100 com zona morta central.
2. Lê botões (pull-up; 0 = pressionado).
3. Calcula `vel_esq` e `vel_dir` (tank drive).
4. Monta pacote de 6 bytes e transmite via NRF24L01 PTX com ACK.

### Receptor (Pico RX) — duas tarefas cooperativas
- **Tarefa RF (alta prioridade):** aguarda IRQ do NRF24L01, decodifica campos e aplica PWM/GPIO imediatamente.
- **Tarefa Sensor (baixa prioridade):** lê ADC do sensor de nível a cada 500 ms; aciona LED e buzzer se abaixo do limiar.
- **Watchdog:** desliga todos os motores e bomba se nenhum pacote válido chegar em 500 ms (failsafe).

---

## 9. Convenção de Commits

Este projeto adota o padrão **[Conventional Commits](https://www.conventionalcommits.org/)** para manter um histórico claro e geração automática de changelogs.

### Formato

```
<tipo>(<escopo>): <descrição curta>

[corpo opcional — explica o contexto e motivação da mudança]

[rodapé opcional — ex.: Refs #issue, BREAKING CHANGE: ...]
```

### Tipos permitidos

| Tipo | Quando usar |
|------|------------|
| `feat` | Nova funcionalidade no firmware ou na documentação |
| `fix` | Correção de bug no firmware ou na lógica do sistema |
| `docs` | Alterações apenas em documentação (README, HTML, Markdown) |
| `style` | Formatação, identação, espaços — sem mudança de lógica |
| `refactor` | Refatoração de código sem adição de feature ou correção de bug |
| `test` | Adição ou modificação de testes |
| `chore` | Tarefas de manutenção: atualizar dependências, configurar ambiente |
| `hw` | Alterações em arquivos de hardware (esquemático, lista de materiais) |
| `perf` | Melhorias de desempenho (ex.: ajuste de PWM, tempo de polling) |

### Escopos sugeridos

| Escopo | Descrição |
|--------|-----------|
| `tx` | Firmware do transmissor |
| `rx` | Firmware do receptor |
| `rf` | Módulo de comunicação NRF24L01 |
| `motor` | Controle de motores / L298N |
| `bomba` | Sistema de bomba e relé |
| `sensor` | Sensor de nível / alertas |
| `docs` | Documentação (HTML, Markdown) |
| `hw` | Hardware e pinagem |
| `ci` | Configurações de CI/CD |

### Exemplos

```
feat(rx): adicionar failsafe com watchdog de 500ms

Se nenhum pacote RF válido for recebido em 500ms, todos os motores
são desligados e a bomba é desativada por segurança.

feat(tx): implementar mapeamento tank drive do joystick

fix(rf): corrigir inicialização do NRF24L01 após reset de hardware

docs(docs): adicionar aba de diagramas de bloco no index.html

hw(rx): atualizar pinagem do L298N #2 para GP16–GP21

chore: adicionar .gitignore para arquivos de ambiente MicroPython

style(tx): formatar indentação e remover espaços extras
```

### Regras gerais

- A **descrição curta** deve estar em **português**, no **imperativo** e sem ponto final.
  - ✅ `feat(rx): adicionar leitura do sensor de nível`
  - ❌ `feat(rx): Adicionei a leitura do sensor de nível.`
- Limite a linha do cabeçalho a **72 caracteres**.
- Use o corpo para explicar **o quê** e **por quê**, não o como.
- Commits com `BREAKING CHANGE:` no rodapé indicam mudanças incompatíveis com versões anteriores.

---

## 10. Política de Tags e Versões

O projeto utiliza **[Semantic Versioning (SemVer)](https://semver.org/)** no formato `vMAJOR.MINOR.PATCH`.

### Regras de versionamento

| Componente | Quando incrementar |
|-----------|-------------------|
| **MAJOR** | Mudança incompatível com versão anterior — ex.: alteração no formato do pacote RF que quebra compatibilidade TX↔RX |
| **MINOR** | Nova funcionalidade adicionada de forma retrocompatível — ex.: novo campo no pacote, novo modo de operação |
| **PATCH** | Correção de bug retrocompatível — ex.: ajuste de deadzone, correção de inicialização |

### Estrutura de tags

```
v<MAJOR>.<MINOR>.<PATCH>[-<pre-release>]

Exemplos:
  v0.1.0          — primeira entrega funcional (RF + motores)
  v0.2.0          — integração da bomba e sensor de nível
  v0.2.1          — correção de bug no failsafe
  v1.0.0          — sistema validado e aprovado para apresentação
  v1.0.0-rc.1     — release candidate antes da apresentação final
```

### Milestones de versão planejadas

| Tag | Semana | Descrição |
|-----|:------:|-----------|
| `v0.1.0` | 5–6 | Comunicação RF funcionando — TX envia, RX recebe |
| `v0.2.0` | 7–8 | Controle de motores via PWM funcional |
| `v0.3.0` | 9–10 | Bomba, relé e sensor de nível integrados |
| `v0.4.0` | 11–12 | Sistema integrado com failsafe e watchdog |
| `v1.0.0-rc.1` | 13–14 | Release candidate — ajustes e calibração |
| `v1.0.0` | 15–16 | Versão final — apresentação |

### Como criar uma tag

```bash
# Criar tag anotada (recomendado)
git tag -a v0.1.0 -m "feat: primeira versão funcional da comunicação RF"

# Enviar tag para o repositório remoto
git push origin v0.1.0

# Enviar todas as tags de uma vez
git push origin --tags
```

### Branches

| Branch | Propósito |
|--------|-----------|
| `main` | Código estável e testado — apenas merges via PR |
| `develop` | Branch de integração contínua |
| `feat/<nome>` | Novas funcionalidades — ex.: `feat/sensor-nivel` |
| `fix/<nome>` | Correções de bug — ex.: `fix/failsafe-timeout` |
| `hw/<nome>` | Alterações de hardware — ex.: `hw/esquematico-v2` |
| `docs/<nome>` | Atualizações de documentação |

---

## 11. Cronograma

| Semana | Período | Etapa | Responsável | Status |
|:------:|---------|-------|-------------|:------:|
| 1–2 | 11/03 – 22/03 | Levantamento de requisitos, aquisição de componentes | Todos | ⏳ Pendente |
| 3–4 | 23/03 – 05/04 | Montagem do chassi 4WD e fiação dos motores + L298N | [Nome 3] | ⏳ Pendente |
| 5–6 | 06/04 – 19/04 | Configuração e teste da comunicação RF (NRF24L01 + Pico) | [Nome 2] | ⏳ Pendente |
| 7–8 | 20/04 – 03/05 | Firmware do receptor: controle de motores via PWM | [Nome 1] | ⏳ Pendente |
| 9–10 | 04/05 – 17/05 | Integração da bomba d'água, relé e sensor de nível | [Nome 1] | ⏳ Pendente |
| 11–12 | 18/05 – 31/05 | Integração geral do sistema e testes de validação | Todos | ⏳ Pendente |
| 13–14 | 01/06 – 14/06 | Ajustes finais, failsafe, calibração de parâmetros | Todos | ⏳ Pendente |
| 15 | 15/06 – 21/06 | Preparação da apresentação e finalização da documentação | [Nome 4] | ⏳ Pendente |
| 16 | 22/06+ | Apresentação final | Todos | ⏳ Pendente |

---

## 12. Orçamento Total Estimado

| Categoria | Itens | Subtotal (R$) |
|-----------|-------|:------------:|
| Microcontroladores | 2× Raspberry Pi Pico | 70,00 |
| Motores e driver | 4× Motor DC + 2× L298N | 62,00 |
| Comunicação RF | 2× NRF24L01 | 24,00 |
| Sistema de água | Bomba + Relé + Sensor + Reservatório | 39,00 |
| Alimentação | 2× Baterias + Regulador DC-DC | 73,00 |
| Estrutura | Chassi 4WD + Protoboard | 60,00 |
| Controle | Joystick + Botões | 14,00 |
| Miscelânea | Jumpers, LEDs, buzzer, fios, resistores | 20,00 |
| **TOTAL** | | **R$ 362,00** |

> Preços estimados com base em valores de mercado nacional (Mercado Livre, Baú da Eletrônica, Robocore) em março de 2026.

---

## 13. Referências Bibliográficas

1. **Raspberry Pi Ltd.** *Raspberry Pi Pico Datasheet*. Disponível em: https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
2. **Raspberry Pi Ltd.** *RP2040 Datasheet*. Disponível em: https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf
3. **STMicroelectronics.** *L298N Dual Full-Bridge Driver Datasheet*. Disponível em: https://www.st.com/resource/en/datasheet/l298.pdf
4. **Nordic Semiconductor.** *nRF24L01+ Product Specification v1.0*. Disponível em: https://www.nordicsemi.com/products/nrf24l01
5. **MicroPython Project.** *MicroPython Documentation for RP2*. Disponível em: https://docs.micropython.org/en/latest/rp2/quickref.html
6. **micropython-nrf24l01 Library.** Disponível em: https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/radio/nrf24l01
7. **Conventional Commits Specification v1.0.0.** Disponível em: https://www.conventionalcommits.org/pt-br/v1.0.0/
8. **Semantic Versioning 2.0.0.** Disponível em: https://semver.org/lang/pt-BR/

---

*Documento gerado em 11 de março de 2026.*
