import hashlib
import random
from functools import reduce
from sympy import isprime

# Utilidade para gerar números primos simples
def generate_small_prime(min_val=100, max_val=200):
    while True:
        p = random.randint(min_val, max_val)
        if isprime(p):
            return p

# Função hash (usando SHA-256 como substituto de SM3)
def H(*args):
    combined = ''.join(map(str, args)).encode()
    return int(hashlib.sha256(combined).hexdigest(), 16)

# Exponenciação modular rápida
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# Etapa 1: Inicialização do sistema
def init_system():
    p = generate_small_prime()
    q = generate_small_prime()
    while q == p:
        q = generate_small_prime()
    
    n = p * q * (p - 1) * (q - 1)
    m = p * q

    # ISRSAC: escolha de 'r', 'alpha(n)', 'e', 'd'
    r = random.randint(2, min(p, q) // 2)
    alpha_n = ((p - 1) * (q - 1) * (p - 2*r) * (q - 2*r)) // (2 * r)

    while True:
        e = random.randint(3, alpha_n - 1)
        if math.gcd(e, alpha_n) == 1:
            break

    d = pow(e, -1, alpha_n)

    return {'p': p, 'q': q, 'n': n, 'm': m, 'e': e, 'd': d}

# Simulação de uma assinatura por difusão
def broadcast_multi_signature(message, signers):
    sys_params = init_system()
    e, n, m, d = sys_params['e'], sys_params['n'], sys_params['m'], sys_params['d']

    # Cada signer cria uma identidade IDi e certificado Si
    signer_data = []
    for i in range(signers):
        IDi = f"user_{i+1}"
        hi = H(IDi)
        Si = mod_exp(hi, d, n)  # certificado
        signer_data.append({'IDi': IDi, 'hi': hi, 'Si': Si})

    # Cada signer escolhe r aleatório e calcula Ri = r^e mod n
    R_list = []
    r_values = []
    for _ in range(signers):
        r = random.randint(2, n - 1)
        r_values.append(r)
        R = mod_exp(r, e, n)
        R_list.append(R)

    # Receptor calcula K = R1 * R2 * ... * Rn mod n
    K = reduce(lambda x, y: (x * y) % n, R_list)

    # K e M são usados para gerar o hash l
    l = H(K, message)

    # Cada signer calcula Di = r * Si^l mod n
    D_list = []
    for i in range(signers):
        Si = signer_data[i]['Si']
        r = r_values[i]
        Di = (r * mod_exp(Si, l, n)) % n
        D_list.append(Di)

    # Receptor junta todas as assinaturas: D = D1 * D2 * ... * Dn mod n
    D = reduce(lambda x, y: (x * y) % n, D_list)

    # Verificação
    h_product = reduce(lambda x, y: x * y, [data['hi'] for data in signer_data])
    K_prime = mod_exp(D, e * h_product * l, m)
    l_prime = H(message, K_prime)

    print(f"Mensagem original: {message}")
    print(f"Assinatura final: D = {D}")
    print(f"Verificação: l == l' ? {l == l_prime}")
    print("Assinatura válida!" if l == l_prime else "Assinatura inválida!")

# Executar a simulação
import math
broadcast_multi_signature("Contrato de parceria", signers=3)