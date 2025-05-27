import random
import hashlib
from sympy import isprime, randprime

# -----------------------------
# Função para gerar os parâmetros p e q
# q: primo de bits especificado (ex.: 160 bits)
# p: número tal que p = k * q + 1 também seja primo
# -----------------------------
def generate_params(bits=160):
    while True:
        # Gera um número primo q com 'bits' bits
        q = randprime(2**(bits-1), 2**bits)
        
        # Tenta encontrar p = k*q + 1 que seja primo
        for k in range(2, 1000):
            p = k * q + 1
            if isprime(p):
                return p, q

# -----------------------------
# Função para encontrar um gerador g do subgrupo de ordem q em Z_p*
# -----------------------------
def find_generator(p, q):
    # Testa possíveis candidatos h
    for h in range(2, p-1):
        # Calcula g = h^((p-1)//q) mod p
        g = pow(h, (p-1)//q, p)
        if g != 1:
            return g
    raise Exception("Generator not found")

# -----------------------------
# Função hash H: aplica SHA-256 aos argumentos concatenados
# Retorna um inteiro correspondente ao digest
# -----------------------------
def H(*args):
    data = ''.join(map(str, args)).encode()
    return int(hashlib.sha256(data).hexdigest(), 16)

# -----------------------------
# Função para calcular o produto modular de uma lista
# -----------------------------
def prod(lst, mod):
    p = 1
    for x in lst:
        p = (p * x) % mod
    return p

# -----------------------------
# Geração dos parâmetros públicos
# -----------------------------
print("Gerando parâmetros, aguarde...")
p, q = generate_params(160)  # Gera p e q
g = find_generator(p, q)     # Encontra gerador g

# Exibe parâmetros gerados
print(f"p = {p}")
print(f"q = {q}")
print(f"g = {g}")

# Número de signatários (participantes da assinatura conjunta)
num_signatarios = 3

# Mensagem a ser assinada
M = "Evento crítico na rede veicular"

# -----------------------------
# Geração das chaves dos signatários
# Cada signatário tem:
#   x: chave privada (secreta)
#   X = g^x mod p: chave pública
# -----------------------------
chaves = []
for _ in range(num_signatarios):
    x = random.randint(1, q-1)  # chave privada
    X = pow(g, x, p)            # chave pública
    chaves.append({'x': x, 'X': X})

# -----------------------------
# Cada signatário gera um nonce r e calcula R = g^r mod p
# -----------------------------
for k in chaves:
    k['r'] = random.randint(1, q-1)  # nonce aleatório
    k['R'] = pow(g, k['r'], p)       # R_i = g^r_i mod p

# Produto modular de todos os R_i
# R = R1 * R2 * ... * Rn mod p
R = prod([k['R'] for k in chaves], p)

# -----------------------------
# Cálculo do hash e da assinatura conjunta
# -----------------------------
e = H(R, M) % q  # Hash da concatenação de R e da mensagem, reduzido mod q

# Cada signatário calcula sua parte da assinatura:
# s_i = r_i + e * x_i mod q
for k in chaves:
    k['s'] = (k['r'] + e * k['x']) % q

# Assinatura conjunta: soma modular de todas as s_i
s = sum(k['s'] for k in chaves) % q

# -----------------------------
# Parâmetro de controle: permite alterar a assinatura para torná-la inválida
# -----------------------------
alterar_assinatura = False  # Troque para True para forçar uma assinatura inválida

if alterar_assinatura:
    s_ver = (s + 1) % q  # Modifica a assinatura (inválida)
else:
    s_ver = s  # Mantém assinatura válida

# -----------------------------
# Verificação da assinatura:
# Checa se g^s mod p == R * (prod X_i)^e mod p
# -----------------------------
left = pow(g, s_ver, p)  # g^s mod p
# Produto das chaves públicas
right = (R * pow(prod([k['X'] for k in chaves], p), H(R, M) % q, p)) % p

# Exibe resultados
print(f"\ng^s mod p: {left}")
print(f"R * (prod X_i)^e mod p: {right}")

# Verifica se a assinatura conjunta é válida
if left == right:
    print("Assinatura válida!")
else:
    print("Assinatura inválida!")
