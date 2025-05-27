import hashlib
import random
import math
from sympy import nextprime

# Função hash H: transforma as entradas em um número grande e pseudoaleatório
def H(*args) -> int:
    msg = ''.join(map(str, args))
    return int(hashlib.sha256(msg.encode()).hexdigest(), 16)

# Algoritmo de Euclides Estendido
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

# Função para calcular o inverso modular
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Inverso modular não existe')
    else:
        return x % m

# Geração das chaves para cada usuário
def generate_keys(bit_length=64):
    p = nextprime(random.getrandbits(bit_length))
    q = nextprime(random.getrandbits(bit_length))
    n = p * q * (p - 1) * (q - 1)  # Módulo de segurança
    m = p * q  # Produto simples dos primos
    r = random.randint(2, min(p, q) // 2)
    alpha_n = ((p - 1)*(q - 1)*(p - 2*r)*(q - 2*r)) // (2*r)
    e = random.randrange(2, alpha_n)
    while math.gcd(e, alpha_n) != 1:
        e = random.randrange(2, alpha_n)
    d = modinv(e, alpha_n)
    return {'public': (e, n), 'private': (d, m), 'modulus': n}

# Geração do certificado: assinatura do ID do usuário com a chave privada
def sign_certificate(ID, d, n):
    hi = H(ID)  # Hash do ID
    Si = pow(hi, d, n)  # Assinatura: hi^d mod n
    return (ID, Si)

# Assinatura multissequencial, com explicação de cada passo
def sequential_signature_verbose(M, user_keys):
    n = user_keys[0]['modulus']  # Todos os usuários usam o mesmo n
    e = user_keys[0]['public'][0]
    m = user_keys[0]['private'][1]
    D = None
    K = None
    f_prev = 1  # Inicializa f

    print(f"\nMensagem a ser assinada: '{M}'")
    print("="*70)

    for i, keys in enumerate(user_keys):
        ID, Si = keys['cert']
        hi = H(ID)  # Hash do ID
        ri = random.randint(2, n - 1)  # Valor aleatório para esta assinatura

        print(f"\nUsuário {ID} ({i+1}º a assinar):")
        print(f"  hi = H(ID) = {hi} (hash do identificador)")
        print(f"  ri = {ri} (valor aleatório gerado pelo usuário)")

        if i == 0:
            K = pow(ri, e, n)  # Inicializa K = r^e mod n
            mi = H(M, K)  # Hash da mensagem com K
            D = (ri * pow(Si, mi, n)) % n  # Produto inicial
            print(f"  K = r^e mod n = {K}")
            print(f"  m = H(M, K) = {mi}")
            print(f"  D = r * S^m mod n = {D}")
        else:
            K = (K * pow(ri, e, n)) % n  # Atualiza K
            mi = H(M, K)
            D = (D * ri * pow(Si, mi, n)) % n
            print(f"  K = K * r^e mod n = {K}")
            print(f"  m = H(M, K) = {mi}")
            print(f"  D = D * r * S^m mod n = {D}")

        f_prev = pow(hi, mi, n)
        print(f"  f = h^m mod n = {f_prev} (valor final parcial para este usuário)")

    print("="*70)
    print("Assinatura Final Gerada:")
    print(f"  K = {K} (valor acumulado das potências dos ri)")
    print(f"  m = {mi} (último hash H(M, K))")
    print(f"  D = {D} (produto acumulado da assinatura)")
    print(f"  f = {f_prev} (último cálculo h^m mod n)\n")

    return (K, mi, D, f_prev)

# Verificação da assinatura
def verify_signature(M, user_keys, signature):
    K, mi, D, f = signature
    n = user_keys[0]['modulus']
    e = user_keys[0]['public'][0]

    print("\nIniciando verificação da assinatura...")
    print("="*70)

    print("Parâmetros recebidos da assinatura:")
    print(f"  K = {K}")
    print(f"  m = {mi}")
    print(f"  D = {D}")
    print(f"  f = {f}")

    print("\nCertificados dos usuários:")
    for i, keys in enumerate(user_keys):
        ID, Si = keys['cert']
        hi = H(ID)
        print(f"Usuário {ID}:")
        print(f"  h = {hi}")
        print(f"  S = {Si}")

    recomputed_m = H(M, K)
    print(f"\nRecomputando m = H(M, K): {recomputed_m}")

    if recomputed_m == mi:
        print("Verificação bem-sucedida: o hash m está consistente com a mensagem e K.")
    else:
        print("Verificação falhou: o hash m não corresponde ao esperado.")

    

# Execução principal
if __name__ == "__main__":
    user_ids = ['U1', 'U2', 'U3']
    user_keys = []

    print("Gerando chaves e certificados...\n")
    for ID in user_ids:
        keys = generate_keys()
        keys['cert'] = sign_certificate(ID, keys['private'][0], keys['modulus'])
        user_keys.append(keys)
        print(f"Chaves geradas para usuário {ID}")

    mensagem = "Contrato de Parceria 2025"
    assinatura_final = sequential_signature_verbose(mensagem, user_keys)

    verify_signature(mensagem, user_keys, assinatura_final)
