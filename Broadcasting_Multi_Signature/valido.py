import random
import hashlib
from math import gcd

# Função de hash (SHA-256) convertida para inteiro
def H(*args):
    data = ''.join(map(str, args))
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)

# Inverso modular
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Inverso modular não existe')
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = extended_gcd(b % a, a)
    return g, x - (b // a) * y, y

# Parâmetros simplificados
p, q = 932483275817587389758923587245, 932483275817587389758923587246
n = p * q * (p - 1) * (q - 1)
m = p * q
phi_n = (p - 1) * (q - 1)
e = 65537
d = modinv(e, phi_n)

# Chaves
public_key = (e, n)
private_key = (d, m)

# Signatários
num_signatarios = 3
signatarios = [{'ID': f'User{i+1}', 'S': random.randint(2, n-1)} for i in range(num_signatarios)]

M = "Evento crítico na rede veicular"

# Geração da assinatura
for s in signatarios:
    s['r'] = random.randint(2, n-1)
    s['R'] = pow(s['r'], e, n)
R_values = [s['R'] for s in signatarios]
K = 1
for R in R_values:
    K = (K * R) % n
l = H(K, M)
for s in signatarios:
    s['D'] = (s['r'] * s['S']) % n
D_values = [s['D'] for s in signatarios]
D = 1
for Di in D_values:
    D = (D * Di) % n

# ======= Verificação simplificada =======
K_prime = pow(D, e * l, m)
l_prime = H(M, K_prime)

print("\n=== RESULTADO DA VERIFICAÇÃO ===")
if l == l_prime:
    print("Assinatura VÁLIDA!")
    print("Explicação: A assinatura foi válida porque K' calculado na verificação resultou no mesmo valor de hash l' que foi obtido na assinatura (l == l').")
else:
    print("Assinatura INVÁLIDA!")

# Exibindo parâmetros importantes
print("\n=== PARÂMETROS ===")
print(f"Chave pública: e = {e}, n = {n}")
print(f"Mensagem: {M}")
print(f"K: {K}")
print(f"D: {D}")
print(f"K' (verificado): {K_prime}")
print(f"l (original): {l}")
print(f"l' (verificado): {l_prime}")