import random
import hashlib
from math import gcd

# -------------------------------
# Funções auxiliares
# -------------------------------

def generate_large_prime():
    primes = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
    return random.choice(primes)

def H(*args):
    data = ''.join(map(str, args))
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Inverso modular não existe')
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a) * y, y)

# -------------------------------
# Estabelecimento do Sistema
# -------------------------------

# Escolhe dois primos grandes p, q (p > 3)
p = generate_large_prime()
while p <= 3:
    p = generate_large_prime()

q = generate_large_prime()
while q == p:
    q = generate_large_prime()

# Calcula n e m conforme a fórmula
n = p * q * (p - 1) * (q - 1)
m = p * q

# Totiente para cálculo de chaves
phi_n = (p - 1) * (q - 1)

# Chave pública e privada
e = 65537
while gcd(e, phi_n) != 1:
    e = random.randrange(3, phi_n, 2)

d = modinv(e, phi_n)

print(f"Primos p={p}, q={q}")
print(f"n = {n}")
print(f"m = {m}")
print(f"Chave pública (e, n): ({e}, {n})")
print(f"Chave privada (d, m): ({d}, {m})")

# -------------------------------
# Geração da assinatura
# -------------------------------

num_signatarios = 3
signatarios = []

# Cada signatário escolhe segredo S_i
for i in range(num_signatarios):
    S = random.randint(2, n - 1)  # segredo privado S_i
    signatarios.append({
        'ID': f'User{i+1}',
        'S': S
    })

# Mensagem a ser assinada
M = "Evento crítico na rede veicular"

# Cada signatário escolhe nonce r_i e calcula R_i = r_i^e mod n
for s in signatarios:
    s['r'] = random.randint(2, n - 1)
    s['R'] = pow(s['r'], e, n)

# Receptor calcula K = produto dos R_i mod n
K = 1
for s in signatarios:
    K = (K * s['R']) % n

# Cada signatário calcula
# l = H(K, M)  (mesmo para todos)
l = H(K, M)

for s in signatarios:
    # D_i = r_i * S_i^l mod n
    s['D'] = (s['r'] * pow(s['S'], l, n)) % n

# -------------------------------
# Verificação da assinatura
# -------------------------------

# Receptor calcula D = produto dos D_i mod n
D = 1
for s in signatarios:
    D = (D * s['D']) % n

# Calcula hashes dos IDs
h_values = [H(s['ID']) for s in signatarios]

# Produto dos hashes dos IDs
product_h = 1
for h in h_values:
    product_h *= h

# Calcula K' = D^{e * product_h * l} mod m
exponent = e * product_h * l
K_prime = pow(D, exponent, m)

# Recalcula l' = H(M, K')
l_prime = H(M, K_prime)

# -------------------------------
# Resultado da verificação
# -------------------------------

print("\n=== RESULTADO DA ASSINATURA ===")
print(f"Mensagem M: {M}")
print(f"\nValores r_i de cada signatário:")
for i, s in enumerate(signatarios, 1):
    print(f"  Signatário {i} (ID={s['ID']}): r = {s['r']}")

print(f"\nValores R_i (r_i^e mod n):")
for i, s in enumerate(signatarios, 1):
    print(f"  Signatário {i}: R = {s['R']}")

print(f"\nValor combinado K (produto dos R_i mod n): {K}")
print(f"Hash l = H(K, M): {l}")

print(f"\nValores D_i (r_i * S_i^l mod n):")
for i, s in enumerate(signatarios, 1):
    print(f"  Signatário {i}: D = {s['D']}")

print(f"\nAssinatura combinada D (produto dos D_i mod n): {D}")

print(f"\nHashes individuais H(ID_i):")
for i, h in enumerate(h_values, 1):
    print(f"  Signatário {i}: {h}")

print(f"\nProduto dos hashes individuais: {product_h}")

print(f"\nExponente usado na verificação: e * product_h * l = {exponent}")
print(f"Valor calculado K' = D^exponente mod m: {K_prime}")

print(f"\nHash verificado l' = H(M, K'): {l_prime}")

if l == l_prime and K == K_prime:
    print("\nAssinatura VÁLIDA! l == l' e K == K'")
else:
    print("\nAssinatura INVÁLIDA! l != l' ou K != K'")

