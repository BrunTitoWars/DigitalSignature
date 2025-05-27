import random
import hashlib
from Crypto.Util import number

def generate_params(bits=160):
    while True:
        q = number.getPrime(bits)
        for k in range(2, 1000):
            p = k * q + 1
            if number.isPrime(p):
                return p, q

def find_generator(p, q):
    for h in range(2, p-1):
        g = pow(h, (p-1)//q, p)
        if g != 1:
            return g
    raise Exception("Generator not found")

def H(*args):
    data = ''.join(map(str, args)).encode()
    return int(hashlib.sha256(data).hexdigest(), 16)

def prod(lst, mod):
    p = 1
    for x in lst:
        p = (p * x) % mod
    return p

print("Gerando parâmetros, aguarde...")
p, q = generate_params(160)
g = find_generator(p, q)

print(f"p = {p}")
print(f"q = {q}")
print(f"g = {g}")

num_signatarios = 3
M = "Evento crítico na rede veicular"

# Chaves dos signatários
chaves = []
for _ in range(num_signatarios):
    x = random.randint(1, q-1)
    X = pow(g, x, p)
    chaves.append({'x': x, 'X': X})

# Nonces e valores R_i
for k in chaves:
    k['r'] = random.randint(1, q-1)
    k['R'] = pow(g, k['r'], p)

R = prod([k['R'] for k in chaves], p)

# Hash e assinatura
e = H(R, M) % q
for k in chaves:
    k['s'] = (k['r'] + e * k['x']) % q

s = sum(k['s'] for k in chaves) % q

# --- Parâmetro para alterar a assinatura ---
alterar_assinatura = False  # Troque para True para alterar e invalidar a assinatura

if alterar_assinatura:
    s_ver = (s + 1) % q  # Altera o valor da assinatura, tornando inválida
else:
    s_ver = s

# Verificação
left = pow(g, s_ver, p)
right = (R * pow(prod([k['X'] for k in chaves], p), H(R, M) % q, p)) % p

print(f"\ng^s mod p: {left}")
print(f"R * (prod X_i)^e mod p: {right}")

if left == right:
    print("Assinatura válida!")
else:
    print("Assinatura inválida!")
