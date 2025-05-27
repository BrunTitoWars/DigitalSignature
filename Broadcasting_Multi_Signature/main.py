import random
import hashlib
from math import gcd
from functools import reduce

# Função hash H(·)
def H(*args):
    data = ''.join(map(str, args)).encode()
    return int(hashlib.sha256(data).hexdigest(), 16)

# Função para encontrar um inverso modular
def modinv(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise Exception('Inverso modular não existe')
    return x % m

# Algoritmo extendido de Euclides
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

# Geração de primos pequenos para exemplo
def generate_prime(min_value=5, max_value=50):
    from sympy import isprime
    while True:
        p = random.randint(min_value, max_value)
        if isprime(p):
            return p

# Etapa 1: Estabelecimento do Sistema
p = generate_prime()
q = generate_prime()
while q == p:
    q = generate_prime()

n = p * q * (p - 1) * (q - 1)
m = p * q

r = random.randint(2, n - 1)
while gcd(r, n) != 1:
    r = random.randint(2, n - 1)

e = random.randint(2, n - 1)
while gcd(e, n) != 1:
    e = random.randint(2, n - 1)

alpha_n = n  # simplificação
d = modinv(e, alpha_n)

public_key = (e, n)
private_key = (d, m)

print(f'Chave pública: {public_key}')
print(f'Chave privada: {private_key}')

# Mensagem e identidades dos signatários
M = "Evento Importante"
num_signatarios = 3
IDs = [f"ID{i+1}" for i in range(num_signatarios)]

# Simulação de chaves privadas dos signatários (Si)
Sis = [random.randint(2, n - 1) for _ in range(num_signatarios)]

# Etapa 2: Geração da Assinatura

# Passo 1: Cada signatário escolhe r e calcula Ri
rs = [random.randint(2, n - 1) for _ in range(num_signatarios)]
Ris = [pow(r, e, n) for r in rs]

# Passo 2: Ur calcula K = R1 * R2 * ... * Rn mod n
K = reduce(lambda x, y: (x * y) % n, Ris)

# Passo 3: Cada signatário calcula l e Di
l = H(K, M)
Dis = [(r * pow(Si, l, n)) % n for r, Si in zip(rs, Sis)]

# Etapa 3: Verificação da Assinatura

# Ur calcula D = D1 * D2 * ... * Dn
D = reduce(lambda x, y: (x * y) % n, Dis)

# h1, h2, ..., hn
hs = [H(ID) for ID in IDs]
prod_hs = reduce(lambda x, y: x * y, hs)

# K' = D^(e * h1 * h2 * ... * hn * l) mod m
exp = e * prod_hs * l
K_prime = pow(D, exp, m)

# l' = H(M, K')
l_prime = H(M, K_prime)

# Verificação
if l == l_prime:
    print("Assinatura VERIFICADA com sucesso!")
else:
    print("FALHA na verificação da assinatura.")
