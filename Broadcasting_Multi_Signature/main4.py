import random
import hashlib
from math import gcd
import time
import matplotlib.pyplot as plt

# Função para gerar primos grandes simplificados
def generate_large_prime():
    primes = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
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

# Função principal
def broadcasting_multisignature():
    times = {}
    start = time.time()

    # Estabelecimento do sistema
    p = generate_large_prime()
    q = generate_large_prime()
    while q == p:
        q = generate_large_prime()
    
    n = p * q * (p - 1) * (q - 1)
    m = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537
    while gcd(e, phi_n) != 1:
        e = random.randrange(3, phi_n, 2)

    d = modinv(e, phi_n)
    
    public_key = (e, n)
    private_key = (d, m)

    num_signatarios = 3
    signatarios = []
    for i in range(num_signatarios):
        signatarios.append({
            'ID': f'User{i+1}',
            'S': random.randint(2, n - 1)
        })

    M = "Evento crítico na rede veicular"

    times['setup'] = time.time() - start
    start = time.time()

    # Geração da assinatura
    for s in signatarios:
        s['r'] = random.randint(2, n - 1)
        s['R'] = pow(s['r'], e, n)
    
    R_values = [s['R'] for s in signatarios]
    K = 1
    for R in R_values:
        K = (K * R) % n
    
    l = H(K, M)

    for s in signatarios:
        s['D'] = (s['r'] * pow(s['S'], l, n)) % n

    D_values = [s['D'] for s in signatarios]
    
    times['generation'] = time.time() - start
    start = time.time()

    # Verificação
    D = 1
    for Di in D_values:
        D = (D * Di) % n

    h_values = [H(s['ID']) for s in signatarios]
    product_h = 1
    for h in h_values:
        product_h *= h

    exponent = e * product_h * l
    K_prime = pow(D, exponent, m)

    l_prime = H(M, K_prime)
    
    is_valid = l == l_prime
    times['verification'] = time.time() - start

    # Exibição dos dados
    print("\nParâmetros do Sistema:")
    print(f"p = {p}, q = {q}")
    print(f"n = {n}")
    print(f"Chave pública: e = {e}, n = {n}")
    print(f"Chave privada: d = {d}, m = {m}\n")

    print("Signatários e componentes:")
    for i, s in enumerate(signatarios, 1):
        print(f"Signatário {i}: ID = {s['ID']}, S = {s['S']}, r = {s['r']}, R = {s['R']}, D = {s['D']}")

    print(f"\nMensagem: {M}")
    print(f"Hash l: {l}")
    print(f"K calculado: {K}")
    print(f"D combinado: {D}")
    print(f"K' verificado: {K_prime}")
    print(f"l' verificado: {l_prime}")

    if is_valid:
        print("\nAssinatura VÁLIDA!")
    else:
        print("\nAssinatura INVÁLIDA!")

    return signatarios, times, n

# Executa o protocolo e coleta dados
signatarios, times, n = broadcasting_multisignature()

# Preparação para o gráfico
import matplotlib.pyplot as plt

ids = [s['ID'] for s in signatarios]
R_values = [s['R'] for s in signatarios]
D_values = [s['D'] for s in signatarios]

plt.figure(figsize=(10, 6))

# Gráfico de valores de R e D
plt.bar(ids, R_values, color='skyblue', label='R valores', alpha=0.7)
plt.bar(ids, D_values, color='salmon', label='D valores', alpha=0.7, bottom=R_values)

plt.xlabel('Signatários')
plt.ylabel('Valores de Chave')
plt.title('Broadcasting Multi-signature: Componentes de Chave')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()

# Gráfico de tempos
plt.figure(figsize=(8, 4))
plt.bar(times.keys(), times.values(), color='green', alpha=0.6)
plt.xlabel('Etapas')
plt.ylabel('Tempo (s)')
plt.title('Tempo de execução por etapa')
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()