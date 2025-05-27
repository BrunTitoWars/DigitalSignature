import math
import time
import matplotlib.pyplot as plt
from sympy import factorint, nextprime

# Funções auxiliares
def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

def inverso_modular(a, m):
    return pow(a, -1, m)

def fatorar(n):
    return list(factorint(n).keys())

def gerar_chaves_isrsac(p, q, r):
    n = p * q * (p - 1) * (q - 1)
    m = p * q
    alpha_n = ((p - 1) * (q - 1) * (p - 2*r) * (q - 2*r)) // (2 * r)
    e = 3
    while mdc(e, alpha_n) != 1:
        e += 2
    d = inverso_modular(e, alpha_n)
    return (e, m), (d, m), n

def assinar_isrsac(hash_msg, chave_privada):
    d, m = chave_privada
    return pow(hash_msg, d, m)

def verificar_isrsac(hash_msg, assinatura, chave_publica):
    e, m = chave_publica
    return pow(assinatura, e, m) == hash_msg

base = 10**4
p = nextprime(2 * base)
q = nextprime(p + 1000)
r = 5

pub_isrsac, priv_isrsac, n_isrsac = gerar_chaves_isrsac(p, q, r)
m_isrsac = pub_isrsac[1]
hash_mensagem_isrsac = 42 % m_isrsac
assinatura_isrsac = assinar_isrsac(hash_mensagem_isrsac, priv_isrsac)
valida_isrsac = verificar_isrsac(hash_mensagem_isrsac, assinatura_isrsac, pub_isrsac)

print("Fatorando módulo ISRSAC...")
inicio_isrsac = time.perf_counter()
fatores_isrsac = fatorar(n_isrsac)
tempo_isrsac = time.perf_counter() - inicio_isrsac

print("Módulo n:", n_isrsac)
print("Assinatura válida:", valida_isrsac)
print(f"Tempo de ataque: {tempo_isrsac:.6f} segundos")
print("Fatores:", fatores_isrsac)