import random
import hashlib
from math import gcd

# Função para gerar primos grandes simplificados
def generate_large_prime():
    primes = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149]  # Exemplo: pequenos para simplificação
    return random.choice(primes)

# Função de hash (SHA-256) convertida para inteiro
def H(*args):
    data = ''.join(map(str, args))
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)

# Função para calcular o inverso modular
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Inverso modular não existe')
    else:
        return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

# Configuração inicial (Estabelecimento do Sistema)
p = generate_large_prime()
q = generate_large_prime()
while q == p:
    q = generate_large_prime()

n = p * q * (p - 1) * (q - 1)
m = p * q
phi_n = (p - 1) * (q - 1)

e = 65537  # Valor comum para e
while gcd(e, phi_n) != 1:
    e = random.randrange(3, phi_n, 2)

d = modinv(e, phi_n)

# Centro de poder define as chaves
public_key = (e, n)
private_key = (d, m)

# Simulação de múltiplos signatários
num_signatarios = 3
signatarios = []

for i in range(num_signatarios):
    signatarios.append({
        'ID': f'User{i+1}',
        'S': random.randint(2, n - 1)  # Chave secreta individual
    })

# Mensagem a ser assinada
M = "Evento crítico na rede veicular"

# ======= Geração da Assinatura =======

# Passo 1: Cada signatário escolhe r aleatório e calcula Ri = r^e mod n
for s in signatarios:
    s['r'] = random.randint(2, n - 1)
    s['R'] = pow(s['r'], e, n)

# Envio de R_i para o receptor Ur
R_values = [s['R'] for s in signatarios]

# Passo 2: Ur calcula K = R1 * R2 * ... * Rn mod n
K = 1
for R in R_values:
    K = (K * R) % n

# Ur transmite K para todos

# Passo 3: Cada signatário calcula l = H(K, M), e D_i = r_i * S_i mod n
l = H(K, M)

for s in signatarios:
    s['D'] = (s['r'] * s['S']) % n

D_values = [s['D'] for s in signatarios]

# ======= Verificação da Assinatura =======

# Ur calcula D = D1 * D2 * ... * Dn
D = 1
for Di in D_values:
    D = (D * Di) % n

# A assinatura final é (D, K, l)

# Verificação:

# 1. Calcula h_i = H(ID_i) para cada signatário
h_values = [H(s['ID']) for s in signatarios]

# 2. Calcula K' = D^(e * h1 * h2 * ... * hn * l) mod m
product_h = 1
for h in h_values:
    product_h *= h

exponent = e * product_h * l
K_prime = pow(D, exponent, m)

# 3. Calcula l' = H(M, K')
l_prime = H(M, K_prime)

# Checa se l == l'
if l == l_prime:
    print("Assinatura VÁLIDA!")
else:
    print("Assinatura INVÁLIDA!")

# ======= Exibição dos dados =======
print("\nParâmetros do Sistema:")
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