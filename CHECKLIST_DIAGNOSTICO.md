## CHECKLIST DE DIAGNÓSTICO - NRF24L01

### 1️⃣ VERIFICAÇÃO FÍSICA DE HARDWARE

- [ ] **Capacitor 10µF conectado?**
  - Entre VCC e GND do NRF24L01
  - ISSO É CRÍTICO! Sem ele, o módulo não funciona bem

- [ ] **Fios conectados corretamente?**
  
  **CONTROLE (Pico 1):**
  ```
  NRF24L01          Pico
  ─────────────────────────
  1  GND      →   GND
  2  VCC      →   3.3V (COM CAPACITOR!)
  3  CE       →   GP9
  4  CSN      →   GP5
  5  SCK      →   GP6
  6  MOSI     →   GP7
  7  MISO     →   GP4
  8  IRQ      →   (não conectar)
  ```
  
  **CARRO (Pico 2):**
  ```
  NRF24L01          Pico
  ─────────────────────────
  1  GND      →   GND
  2  VCC      →   3.3V (COM CAPACITOR!)
  3  CE       →   GP12  ← DIFERENTE!
  4  CSN      →   GP5
  5  SCK      →   GP6
  6  MOSI     →   GP7
  7  MISO     →   GP4
  8  IRQ      →   (não conectar)
  ```

- [ ] **Nenhum fio solto ou mal soldado?**
  - Verifique todas as conexões
  - Use multímetro se necessário

### 2️⃣ TESTES DE SOFTWARE

**Ordem recomendada:**

#### PASSO 1: Teste no CONTROLE
```
1. Copie: diagnostico_completo.py → Pico do CONTROLE
2. Execute (deixe rodando por 10s)
3. Veja a saída no console
```

Se o CONTROLE disser **"Módulo não responde"**:
- ❌ Fiação está errada
- ❌ Capacitor não está conectado
- ❌ Módulo NRF24L01 pode estar quebrado

Se o CONTROLE disser **"Envio com sucesso"**:
- ✅ Modulo está OK
- → Vá para PASSO 2

#### PASSO 2: Teste no CARRO
```
1. Copie: diagnostico_completo.py → Pico do CARRO
2. Execute (deixe aguardando)
3. Rode novamente o CONTROLE
```

Se o CARRO disser **"Nenhuma mensagem recebida"**:
- ❌ Receptor pode ter fiação errada
- ❌ Capacitor não está conectado
- ❌ CE está no pino errado (deve ser GP12!)

Se o CARRO disser **"X mensagens recebidas"**:
- ✅ COMUNICAÇÃO FUNCIONANDO!

### 3️⃣ SE AINDA NÃO FUNCIONAR

**Checklist final:**

- [ ] Você colocou um **capacitor 10µF** entre VCC e GND?
- [ ] O **CE do CARRO está em GP12** (não GP9)?
- [ ] Os **pinos SCK/MOSI/MISO** estão iguais nos dois?
- [ ] Os **endereços são iguais?**
  ```
  ADDR_CONTROLE = bytes([0xE7, 0xE7, 0xE7, 0xE7, 0xE7])
  ADDR_CARRO    = bytes([0xC2, 0xC2, 0xC2, 0xC2, 0xC2])
  ```
- [ ] Os **dois Picos estão no CHANNEL 2?**
- [ ] Você **alimenta os Picos corretamente?** (USB ou 5V externo)
- [ ] O **NRF24L01 está alimentado em 3.3V**? (não 5V!)

### 4️⃣ RESULTADO ESPERADO

**CONTROLE console:**
```
[6] TESTE DE ENVIO...
  Enviando: [50, 30, 1, 0]
  ✓ ENVIO COM SUCESSO!
```

**CARRO console:**
```
[6] AGUARDANDO MENSAGENS...
  [1] ✓ RX: X= 50, Y= 30
      ✓ TX: Resposta enviada
```

### ⚡ POTENCIAL PROBLEMA #1: CAPACITOR

**Sintoma:** "send failed" repetido

**Solução:** Adicione capacitor 10µF - 100µF entre VCC e GND do NRF24L01

```
Pico ─[10µF]─ NRF24L01
     GND      VCC   GND
```

### ⚡ POTENCIAL PROBLEMA #2: PIN CE ERRADO

**Sintoma:** CONTROLE: "send failed", CARRO: não recebe nada

**Solução:** Verifique se o CE do CARRO está em **GP12** (não GP9)

### ⚡ POTENCIAL PROBLEMA #3: ALIMENTAÇÃO

**Sintoma:** Módulo não responde

**Solução:** 
- NRF24L01 precisa de **3.3V estável**
- Pico fornece até 500mA pelo pino 3.3V
- Se tem outros componentes, pode ser insuficiente
- Considere usar uma fonte externa 3.3V para o NRF24L01

---

**Qual é a situação?** Você conseguiu executar o `diagnostico_completo.py`?
