import random
import hashlib
from math import gcd
import matplotlib.pyplot as plt
import time

# -------------------------------
# Funções auxiliares
# -------------------------------

# Função para gerar um número primo (pequeno, para simplificação didática)
def generate_large_prime():
    primes = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
    return random.choice(primes)

# Função de hash: transforma vários argumentos em um inteiro via SHA-256
def H(*args):
    data = ''.join(map(str, args))
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)

# Função para calcular o inverso modular (usado na chave privada)
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Inverso modular não existe')
    return x % m

# Algoritmo de Euclides Estendido (para o inverso modular)
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a) * y, y)

# -------------------------------
# Etapa 1: Configuração do sistema
# -------------------------------

start_time = time.time()

# Geração dos primos p e q
p = generate_large_prime()
q = generate_large_prime()
while q == p:
    q = generate_large_prime()

# Cálculo dos parâmetros principais
n = p * q * (p - 1) * (q - 1)  # Módulo para operações
m = p * q                     # Módulo para verificação
phi_n = (p - 1) * (q - 1)     # Totiente de Euler

# Geração da chave pública (e) e privada (d)
e = 65537
while gcd(e, phi_n) != 1:
    e = random.randrange(3, phi_n, 2)
d = modinv(e, phi_n)

public_key = (e, n)
private_key = (d, m)

setup_time = time.time() - start_time

# -------------------------------
# Etapa 2: Geração da assinatura
# -------------------------------

start_gen = time.time()

num_signatarios = 3
signatarios = []

# Criando signatários com IDs e chaves secretas
for i in range(num_signatarios):
    signatarios.append({
        'ID': f'User{i+1}',
        'S': random.randint(2, n - 1)
    })

# Mensagem a ser assinada
M = "Evento crítico na rede veicular"

# Cada signatário escolhe valor aleatório r e calcula R = r^e mod n
for s in signatarios:
    s['r'] = random.randint(2, n - 1)
    s['R'] = pow(s['r'], e, n)

# Receptor calcula K = produto de todos os R mod n
K = 1
for s in signatarios:
    K = (K * s['R']) % n

# Calcula hash l = H(K, M)
l = H(K, M)

# Cada signatário calcula D = r * S mod n
for s in signatarios:
    s['D'] = (s['r'] * s['S']) % n

# Produto final D = D1 * D2 * ... * Dn mod n
D = 1
for s in signatarios:
    D = (D * s['D']) % n

gen_time = time.time() - start_gen

# -------------------------------
# Etapa 3: Verificação da assinatura
# -------------------------------

start_ver = time.time()

# Calcula hash de cada ID
h_values = [H(s['ID']) for s in signatarios]

# Produto dos hashes dos IDs
product_h = 1
for h in h_values:
    product_h *= h

# Calcula K' = D^(e * product_h * l) mod m
exponent = e * product_h * l
K_prime = pow(D, exponent, m)

# Recalcula l' = H(M, K')
l_prime = H(M, K_prime)

ver_time = time.time() - start_ver

# -------------------------------
# Resultado da verificação
# -------------------------------

resultado = "VÁLIDA" if l == l_prime else "INVÁLIDA"
print(f"\nAssinatura {resultado}!\n")

# -------------------------------
# Exibição dos parâmetros
# -------------------------------

print("Parâmetros do Sistema:")
print(f"p = {p}, q = {q}")
print(f"n = {n}")
print(f"Chave pública: e = {e}, n = {n}")
print(f"Chave privada: d = {d}, m = {m}")

print("\nSignatários e componentes:")
for i, s in enumerate(signatarios, 1):
    print(f"Signatário {i}: ID = {s['ID']}, S = {s['S']}, r = {s['r']}, R = {s['R']}, D = {s['D']}")

print(f"\nMensagem: {M}")
print(f"Hash l: {l}")
print(f"K calculado: {K}")
print(f"D combinado: {D}")
print(f"K' verificado: {K_prime}")
print(f"l' verificado: {l_prime}")

# -------------------------------
# Gráfico ilustrativo do processo
# -------------------------------

# Criar figura
fig, ax = plt.subplots(figsize=(10, 6))

# Dados para o gráfico
signatarios_ids = [s['ID'] for s in signatarios]
R_values = [s['R'] for s in signatarios]
D_values = [s['D'] for s in signatarios]

bar_width = 0.35
x = range(len(signatarios))

# Plot das barras de R e D
ax.bar(x, R_values, width=bar_width, label='R valores', color='skyblue')
ax.bar([i + bar_width for i in x], D_values, width=bar_width, label='D valores', color='salmon')

# Adiciona resultado no gráfico
plt.text(0.5, max(R_values + D_values) * 1.1, f'Resultado: Assinatura {resultado}', fontsize=14, ha='center')

# Configurações do gráfico
ax.set_xlabel('Signatários')
ax.set_ylabel('Valores Numéricos')
ax.set_title('Componentes R e D dos Signatários na Assinatura')
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(signatarios_ids)
ax.legend()

plt.tight_layout()
plt.show()

# -------------------------------
# Gráfico de tempo por fase
# -------------------------------

fig, ax = plt.subplots(figsize=(8, 5))
fases = ['Setup', 'Geração', 'Verificação']
tempos = [setup_time, gen_time, ver_time]

ax.bar(fases, tempos, color=['purple', 'green', 'orange'])
ax.set_ylabel('Tempo (s)')
ax.set_title('Tempo de execução por fase do protocolo')

for i, v in enumerate(tempos):
    ax.text(i, v + 0.001, f"{v:.4f}s", ha='center')

plt.tight_layout()
plt.show()