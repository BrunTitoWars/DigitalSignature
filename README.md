
# 🔐 Digital Signature Algorithms based on ISRSAC and RSA

Este repositório contém a implementação de diferentes algoritmos de assinatura digital, incluindo:

- Assinatura Digital baseada no algoritmo **ISRSAC** (uma versão aprimorada do RSA).
- Assinatura Digital padrão com RSA.
- Esquemas de **Multiassinatura Sequencial** e **Multiassinatura de Broadcast**.
- Avaliação comparativa de resistência a ataques de força bruta entre ISRSAC e RSA.

## 📁 Estrutura do Projeto

```
DigitalSignature-main/
│
├── Broadcasting_Multi_Signature/
│   ├── broadcastmultisigncomplotagem.py  # Multiassinatura de Broadcast com plotagem
│   ├── geracaodemultiassinaturas.py       # Geração de assinaturas de broadcast
│   └── schnorrmultisig.py                 # Implementação de multiassinatura Schnorr
│
├── Digital_Signature_based_on_ISRSAC/
│   └── main.py                            # Assinatura Digital baseada em ISRSAC
│
├── Digital_Signature_based_on_RSA/
│   ├── main_with_disturbance.py           # Teste de assinatura com alteração na mensagem
│   └── main_with_no_disturbance.py        # Teste de assinatura sem alteração (válida)
│
├── Evaluation_of_Brute_force_RSA_vs_ISRSAC/
│   └── main.py                            # Simulação de ataque de força bruta comparando RSA e ISRSAC
│
├── Sequential_Multi_Signature/
│   └── sequentialmultisig.py              # Multiassinatura sequencial
│
└── README.md                              # Documentação do projeto
```

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Bibliotecas:**
  - `hashlib` — Função hash (SHA-256)
  - `random` e `math` — Operações matemáticas
  - `cryptography` — Implementação de RSA com padding seguro
  - `matplotlib` — Para geração de gráficos (em scripts de plotagem)

## 🔑 Algoritmos Implementados

### ✔️ ISRSAC (Improved Secure RSA Cryptosystem)
- Extensão do RSA que utiliza um módulo expandido `n = p*q*(p-1)*(q-1)`.
- Aumenta a dificuldade de fatoração do módulo, reforçando a segurança.

### ✔️ Assinatura Digital
- Baseada tanto em ISRSAC quanto no RSA clássico.

### ✔️ Multiassinatura
- **Sequencial:** Cada signatário assina na ordem.
- **Broadcast:** Todos assinam e o coletor agrega as assinaturas.

### ✔️ Proxy Signature (descrita no artigo, não implementada no código)

## 📊 Avaliação de Desempenho

- Comparação do tempo necessário para ataques de força bruta contra RSA e ISRSAC.
- Geração de gráficos que mostram como o ISRSAC oferece maior resistência para tamanhos de chave equivalentes.

## ⚙️ Como Executar

1. Instale as dependências (se necessário):
```bash
pip install cryptography matplotlib
```

2. Execute qualquer script diretamente, exemplo:
```bash
python Digital_Signature_based_on_ISRSAC/main.py
```

3. Para gerar gráficos de comparação:
```bash
python Evaluation_of_Brute_force_RSA_vs_ISRSAC/main.py
```

## 🛠️ Modificações e Adaptações

- Substituição do SM3 (utilizado no artigo original) por SHA-256, devido à compatibilidade e disponibilidade em bibliotecas padrão do Python.
- Scripts adicionais foram criados para validar assinaturas com e sem alteração da mensagem.

## 👨‍💻 Autor

- **João Vitor Russo A. Werneck**  
- **Ricardo André**
- **Arquimedes França**
- **Eduarda Azenha**
- **Alyson Farias**
