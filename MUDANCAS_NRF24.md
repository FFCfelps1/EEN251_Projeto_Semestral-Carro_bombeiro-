# Adaptação para Biblioteca NRF24L01

## Resumo das Mudanças

Ambos os códigos foram adaptados para usar a biblioteca `nrf24l01.py` profissional em vez da implementação customizada. Isso simplifica o código e melhora a confiabilidade.

## Principais Mudanças

### 1. **Importação da Biblioteca**
```python
from nrf24l01 import NRF24L01, POWER_3, SPEED_1M
```

### 2. **Inicialização do Rádio**

**Antes:**
```python
radio = NRF24(spi, csn, ce)  # Classe customizada
```

**Depois:**
```python
radio = NRF24L01(spi, csn, ce, channel=2, payload_size=4)
radio.set_power_speed(POWER_3, SPEED_1M)
```

### 3. **Métodos Utilizados da Biblioteca**

| Método | Função |
|--------|--------|
| `open_tx_pipe(address)` | Configura o endereço para transmissão |
| `open_rx_pipe(pipe_id, address)` | Configura o endereço para recepção |
| `send(data)` | Envia dados (timeout de 500ms por padrão) |
| `recv()` | Recebe dados |
| `any()` | Verifica se há dados disponíveis |
| `start_listening()` | Ativa modo RX |
| `stop_listening()` | Desativa modo RX |

### 4. **Fluxo de Comunicação**

#### Controle (TX/RX cíclico):
1. `stop_listening()` - Sai do modo RX
2. `send(payload)` - Envia comando para o carro
3. `start_listening()` - Volta ao modo RX
4. Aguarda resposta com `radio.any()`
5. Recebe com `radio.recv()`

#### Carro (RX contínuo com TX sob demanda):
1. `start_listening()` - Ativa modo RX na inicialização
2. Aguarda comandos com `radio.any()`
3. Recebe com `radio.recv()`
4. `stop_listening()` - Sai do modo RX para enviar
5. `send(payload_umidade)` - Envia resposta
6. `start_listening()` - Volta ao modo RX

### 5. **Display OLED no Controle**

O display agora mostra os dados de umidade recebidos do carro em tempo real:
- **Umidade %**: Porcentagem do nível de água
- **AGUA/SECO**: Status do sensor digital

Formato da tela:
```
CARRO BOMBEIRO
X:XX
Y:XX
BTN:ON/OFF
UM:XX% AGUA/SECO
```

### 6. **Protocolo de Comunicação**

**Payload enviado pelo controle para o carro (4 bytes):**
- `[0]` = X normalizado (-100 a 100)
- `[1]` = Y normalizado (-100 a 100)
- `[2]` = Botão (0=pressionado, 1=solto)
- `[3]` = Reservado (0)

**Payload enviado pelo carro para o controle (4 bytes):**
- `[0]` = Nível de umidade (0-100%)
- `[1]` = Status digital de água (1=detecção, 0=sem detecção)
- `[2]` = Marcador (0xFF)
- `[3]` = Reservado (0)

## Vantagens da Nova Implementação

✅ **Código mais limpo**: Menos linhas de código, sem necessidade de gerenciar registradores SPI manualmente

✅ **Melhor tratamento de erros**: A biblioteca trata timeouts automaticamente

✅ **Integração com display**: O controle mostra dados de umidade em tempo real

✅ **Comunicação bidirecional simples**: Alternar entre TX/RX é mais intuitivo

✅ **Compatibilidade**: Mesmos endereços e configurações de canal

## Teste de Comunicação

Ambos os códigos estão prontos para usar. O carro aguardará pelo controle, e o controle enviará comandos periodicamente (a cada 100ms). A umidade será exibida no display OLED do controle.

### Console esperado no carro:
```
Receptor pronto, aguardando sinal...
X: 50 | Y: -30 | BOMBA: 0 | Umidade: 75% | AGUA
```

### Console esperado no controle:
```
Aguardando dados...
X: 50 Y: -30 BTN: OFF | Umidade: 75 % AGUA
```
