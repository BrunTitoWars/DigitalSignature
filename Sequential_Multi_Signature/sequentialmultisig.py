import hashlib
import random
import math
from sympy import nextprime

# Função hash H(ID) ou H(M, K)
def H(*args) -> int:
    msg = ''.join(map(str, args))
    return int(hashlib.sha256(msg.encode()).hexdigest(), 16)

# Algoritmo de Euclides Estendido para encontrar o inverso modular
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

# Geração de chaves ISRSAC
def generate_keys(bit_length=64):
    p = nextprime(random.getrandbits(bit_length))
    q = nextprime(random.getrandbits(bit_length))
    n = p * q * (p - 1) * (q - 1)
    m = p * q
    r = random.randint(2, min(p, q) // 2)
    alpha_n = ((p - 1)*(q - 1)*(p - 2*r)*(q - 2*r)) // (2*r)
    e = random.randrange(2, alpha_n)
    while math.gcd(e, alpha_n) != 1:
        e = random.randrange(2, alpha_n)
    d = modinv(e, alpha_n)
    return {'public': (e, n), 'private': (d, m), 'modulus': n}

# Geração do certificado (ID, Si)
def sign_certificate(ID, d, n):
    hi = H(ID)
    Si = pow(hi, d, n)
    return (ID, Si)

# Assinatura multisequencial com saída detalhada no terminal
def sequential_signature_verbose(M, user_keys):
    n = user_keys[0]['modulus']
    e = user_keys[0]['public'][0]
    m = user_keys[0]['private'][1]
    D = None
    K = None
    f_prev = 1

    print(f"\nMensagem a ser assinada: {M}\n{'='*60}")
    for i, keys in enumerate(user_keys):
        ID, Si = keys['cert']
        hi = H(ID)
        ri = random.randint(2, n - 1)
        print(f"\nUsuário {ID} ({i+1}º a assinar):")
        print(f"  hi = H(ID) = {hi}")
        print(f"  ri (aleatório) = {ri}")
        if i == 0:
            K = pow(ri, e, n)
            mi = H(M, K)
            D = (ri * pow(Si, mi, n)) % n
            print(f"  K = r^e mod n = {K}")
            print(f"  m = H(M, K) = {mi}")
            print(f"  D = r * S^m mod n = {D}")
        else:
            K = (K * pow(ri, e, n)) % n
            mi = H(M, K)
            D = (D * ri * pow(Si, mi, n)) % n
            print(f"  K = K * r^e mod n = {K}")
            print(f"  m = H(M, K) = {mi}")
            print(f"  D = D * r * S^m mod n = {D}")
        f_prev = pow(hi, mi, n)
        print(f"  f = h^m mod n = {f_prev}")

    print(f"\n{'='*60}\nAssinatura Final:")
    print(f"  K = {K}")
    print(f"  m = {mi}")
    print(f"  D = {D}")
    print(f"  f = {f_prev}")
    return (K, mi, D, f_prev)

# Execução da simulação
if __name__ == "__main__":
    user_ids = ['U1', 'U2', 'U3']
    user_keys = []
    for ID in user_ids:
        keys = generate_keys()
        keys['cert'] = sign_certificate(ID, keys['private'][0], keys['modulus'])
        user_keys.append(keys)

    mensagem = "Contrato de Parceria 2025"
    assinatura_final = sequential_signature_verbose(mensagem, user_keys)
