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
9. [Como Executar](#9-como-executar)
10. [Convenção de Commits](#10-convenção-de-commits)
11. [Política de Tags e Versões](#11-política-de-tags-e-versões)
12. [Cronograma](#12-cronograma)
13. [Orçamento Total Estimado](#13-orçamento-total-estimado)
14. [Riscos e Limitações](#14-riscos-e-limitações)
15. [Referências Bibliográficas](#15-referências-bibliográficas)

---

## 1. Integrantes e Responsabilidades

| Nome | RA | Função Principal |
|------|----|-----------------|
| [Nome 1] | [RA] | Firmware do Receptor (Pico RX) — motores e bomba |
| [Nome 2] | [RA] | Firmware do Transmissor (Pico TX) — controle RF |
| [Nome 3] | [RA] | Hardware — montagem do chassi e fiação |
| [Nome 4] | [RA] | Integração do sistema e documentação |

> Preencher com os dados reais do grupo.

---

## 2. Descrição Geral do Projeto

O projeto consiste no desenvolvimento de um veículo robótico em escala inspirado em um caminhão de bombeiro, capaz de se locomover de maneira teleoprada por meio de comunicação sem fio RF 2.4 GHz (módulo NRF24L01). O veículo é dotado de tração 4WD com quatro motores DC controlados por dois módulos L298N, uma mini bomba d'água acionável remotamente, e um reservatório de água com sensor de nível que alerta o operador quando a água estiver baixa.

O sistema é dividido em dois blocos principais:

- **Transmissor (controle remoto):** baseado em um Raspberry Pi Pico com joystick analógico e botões, responsável por capturar os comandos do operador e enviá-los via NRF24L01.
- **Receptor (carro):** baseado em um segundo Raspberry Pi Pico que recebe os pacotes RF, interpreta os comandos e aciona os motores, a bomba e os alertas de nível.

Todo o firmware é desenvolvido em **MicroPython**, aproveitando a plataforma Raspberry Pi Pico (microcontrolador RP2040).

---

## 3. Objetivos

### 3.1 Objetivo Geral

Projetar, construir e programar um carro de bombeiro em miniatura, teleoprado por radiofrequência, com sistema de bombeamento de água e monitoramento do nível do reservatório, utilizando a plataforma Raspberry Pi Pico como controlador central.

### 3.2 Objetivos Específicos

- Implementar comunicação bidirecional RF 2.4 GHz entre controle e veículo utilizando o módulo NRF24L01.
- Controlar a velocidade e direção de quatro motores DC via PWM (diferencial de velocidade — tank drive).
- Acionar remotamente uma mini bomba d'água via relé para simular o combate a incêndios.
- Monitorar em tempo real o nível do reservatório de água, com alertas visuais (LED) e sonoros (buzzer).
- Documentar todo o processo de desenvolvimento: hardware, firmware e validação do sistema.

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
| GP2 | 4 | NRF24L01 | SCK (SPI0) | Clock SPI |
| GP3 | 5 | NRF24L01 | MOSI (SPI0) | Dados saída |
| GP4 | 6 | NRF24L01 | MISO (SPI0) | Dados entrada |
| GP5 | 7 | NRF24L01 | CSn | Chip Select |
| GP6 | 9 | NRF24L01 | CE | Chip Enable |
| GP8 | 11 | L298N #1 | ENA (PWM) | Vel. Motor 1 |
| GP9 | 12 | L298N #1 | ENB (PWM) | Vel. Motor 2 |
| GP10–GP13 | 14–17 | L298N #1 | IN1–IN4 | Direção Motores 1/2 |
| GP16 | 21 | L298N #2 | ENA (PWM) | Vel. Motor 3 |
| GP17 | 22 | L298N #2 | ENB (PWM) | Vel. Motor 4 |
| GP18–GP21 | 24–27 | L298N #2 | IN1–IN4 | Direção Motores 3/4 |
| GP22 | 29 | Relé 5V | Sinal | Ativa bomba |
| GP26 | 31 | Sensor nível | ADC0 | Leitura analógica |
| GP27 | 32 | LED alerta | GPIO OUT | Nível baixo |
| GP28 | 34 | Buzzer | GPIO OUT | Alerta sonoro |

### Transmissor — Raspberry Pi Pico (TX)

| Pino | GPIO | Periférico | Sinal | Obs. |
|------|:----:|-----------|-------|------|
| GP2–GP6 | 4–9 | NRF24L01 | SPI0 + CE/CSn | Igual ao RX |
| GP14 | 19 | Botão Bomba | GPIO IN | Pull-up interno |
| GP15 | 20 | Botão Stop | GPIO IN | Pull-up interno |
| GP26 | 31 | Joystick X | ADC0 | Eixo horizontal |
| GP27 | 32 | Joystick Y | ADC1 | Eixo vertical |

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

## 9. Como Executar

### Pré-requisitos
- [Thonny IDE](https://thonny.org/) ou qualquer cliente MicroPython para RP2040
- MicroPython >= 1.22 gravado nos dois Raspberry Pi Pico
- Biblioteca [`nrf24l01`](https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/radio/nrf24l01) copiada para ambos os Picos

### Passos
```bash
# 1. Clone o repositório
git clone https://github.com/<usuario>/EEN251_Projeto_Semestral.git

# 2. Grave o firmware no Pico TX
# Abra firmware/tx/main.py no Thonny e execute no dispositivo

# 3. Grave o firmware no Pico RX
# Abra firmware/rx/main.py no Thonny e execute no dispositivo

# 4. Visualize a documentação
# Abra docs/index.html em qualquer navegador
```

---

## 10. Convenção de Commits

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

## 11. Política de Tags e Versões

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

## 12. Cronograma

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

## 13. Orçamento Total Estimado

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

## 14. Riscos e Limitações

- **Alcance RF:** em ambiente interno com obstáculos, o alcance efetivo pode ser < 15–20 m. A versão PA+LNA eleva para ~100 m em campo aberto.
- **Impermeabilização:** proteger a eletrônica contra respingos da bomba. Posicionar o bico de saída longe dos PCBs.
- **Autonomia:** com 4 motores + bomba simultâneos, corrente pode superar 2 A. Bateria 2S deve ter > 2000 mAh para ~20–30 min.
- **Aquecimento do L298N:** eficiência ~70%. Monitorar temperatura em testes prolongados; considerar dissipador adicional.
- **Latência RF:** Enhanced ShockBurst adiciona ~1–2 ms/pacote — aceitável para controle em malha aberta.
- **Tensão do NRF24L01:** opera em 3,3 V — nunca conectar ao 5V.
- **Sensor resistivo:** eletrodos corroem com uso prolongado. Considerar sensor capacitivo para uso a longo prazo.

---

## 15. Referências Bibliográficas

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
