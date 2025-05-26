import hashlib
import random
from math import gcd


def gerar_primos():
    # Números pequenos para exemplo didático, troque por primos grandes em produção
    primos = [
        101, 103, 107, 109, 113, 127, 131, 137, 139,
        149, 151, 157, 163, 167, 173, 179, 181, 191, 193
    ]
    p = random.choice(primos)
    q = random.choice(primos)
    while p == q:
        q = random.choice(primos)
    return p, q


def calcular_alpha(p, q, r):
    return ((p - 1) * (q - 1) * (p - 2 * r) * (q - 2 * r)) // (2 * r)


def inverso_modular(a, m):
    # Algoritmo extendido de Euclides para inverso modular
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1


def gerar_chaves():
    p, q = gerar_primos()
    n = p * q * (p - 1) * (q - 1)
    m = p * q
    r = random.randint(1, min((p - 1) // 2, (q - 1) // 2))
    alpha = calcular_alpha(p, q, r)

    e = random.randrange(2, alpha)
    while gcd(e, alpha) != 1:
        e = random.randrange(2, alpha)

    d = inverso_modular(e, alpha)

    chave_publica = (e, n)
    chave_privada = (d, m)

    return chave_publica, chave_privada


def hash_mensagem(mensagem):
    h = hashlib.sha256()
    h.update(mensagem.encode('utf-8'))
    return int(h.hexdigest(), 16)


def assinar(mensagem, chave_privada):
    d, n = chave_privada
    h = hash_mensagem(mensagem)
    assinatura = pow(h, d, n)
    return assinatura


def verificar(mensagem, assinatura, chave_publica):
    e, n = chave_publica
    h = hash_mensagem(mensagem)
    verificado = pow(assinatura, e, n)
    return verificado == h


# =====================
# Demonstração do uso
# =====================

# Gerar as chaves
chave_publica, chave_privada = gerar_chaves()

print("Chave Pública (e, n):", chave_publica)
print("Chave Privada (d, m):", chave_privada)

# Mensagem a ser assinada
mensagem = "Esta é uma mensagem confidencial."

# Assinar a mensagem
assinatura = assinar(mensagem, chave_privada)
print("Assinatura:", assinatura)

# Verificar a assinatura
valido = verificar(mensagem, assinatura, chave_publica)
print("A assinatura é válida?", valido)
