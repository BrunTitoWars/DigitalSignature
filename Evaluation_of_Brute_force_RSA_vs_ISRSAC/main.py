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

# RSA
def gerar_chaves_rsa(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while mdc(e, phi) != 1:
        e += 2
    d = inverso_modular(e, phi)
    return (e, n), (d, n)

def assinar_rsa(mensagem, chave_privada):
    d, n = chave_privada
    return pow(mensagem, d, n)

def verificar_rsa(mensagem, assinatura, chave_publica):
    e, n = chave_publica
    return pow(assinatura, e, n) == mensagem

# ISRSAC
def gerar_chaves_isrsac(p, q, r):
    n = p * q * (p - 1) * (q - 1)
    m = p * q
    alpha_n = ((p - 1) * (q - 1) * (p - 2*r) * (q - 2*r)) // (2 * r)
    e = 3
    while mdc(e, alpha_n) != 1:
        e += 2
    d = inverso_modular(e, alpha_n)
    return (e, m), (d, m), n  # assinatura e verificação com m

def assinar_isrsac(hash_msg, chave_privada):
    d, m = chave_privada
    return pow(hash_msg, d, m)

def verificar_isrsac(hash_msg, assinatura, chave_publica):
    e, m = chave_publica
    return pow(assinatura, e, m) == hash_msg

# ISR-RSA
def gerar_chaves_isrrsa(p, q):
    n = p * p * q
    phi = p * (p - 1) * (q - 1)
    e = 3
    while mdc(e, phi) != 1:
        e += 2
    d = inverso_modular(e, phi)
    return (e, n), (d, n)

def assinar_isrrsa(mensagem, chave_privada):
    d, n = chave_privada
    return pow(mensagem, d, n)

def verificar_isrrsa(mensagem, assinatura, chave_publica):
    e, n = chave_publica
    return pow(assinatura, e, n) == mensagem

# -----------------------------
# Demonstração
# -----------------------------
# Gerando primos grandes
base = 10**4
p = nextprime(2 * base)
q = nextprime(p + 1000)
r = 5  # valor seguro e pequeno

# RSA
pub_rsa, priv_rsa = gerar_chaves_rsa(p, q)
n_rsa = pub_rsa[1]
m_rsa = n_rsa
hash_mensagem = 42 % m_rsa  # valor garantido < m
assinatura_rsa = assinar_rsa(hash_mensagem, priv_rsa)
valida_rsa = verificar_rsa(hash_mensagem, assinatura_rsa, pub_rsa)

# ISRSAC
pub_isrsac, priv_isrsac, n_isrsac = gerar_chaves_isrsac(p, q, r)
m_isrsac = pub_isrsac[1]
hash_mensagem_isrsac = 42 % m_isrsac
assinatura_isrsac = assinar_isrsac(hash_mensagem_isrsac, priv_isrsac)
valida_isrsac = verificar_isrsac(hash_mensagem_isrsac, assinatura_isrsac, pub_isrsac)

# ISR-RSA
pub_isrrsa, priv_isrrsa = gerar_chaves_isrrsa(p, q)
n_isrrsa = pub_isrrsa[1]
m_isrrsa = n_isrrsa
hash_mensagem_isrrsa = 42 % m_isrrsa
assinatura_isrrsa = assinar_isrrsa(hash_mensagem_isrrsa, priv_isrrsa)
valida_isrrsa = verificar_isrrsa(hash_mensagem_isrrsa, assinatura_isrrsa, pub_isrrsa)

# Fatorações
print("\nFatorando módulo RSA...")
inicio_rsa = time.perf_counter()
fatores_rsa = fatorar(n_rsa)
tempo_rsa = time.perf_counter() - inicio_rsa

print("Fatorando módulo ISRSAC...")
inicio_isrsac = time.perf_counter()
fatores_isrsac = fatorar(n_isrsac)
tempo_isrsac = time.perf_counter() - inicio_isrsac

print("Fatorando módulo ISR-RSA...")
inicio_isrrsa = time.perf_counter()
fatores_isrrsa = fatorar(n_isrrsa)
tempo_isrrsa = time.perf_counter() - inicio_isrrsa

# Resultados
print("\n=== RSA ===")
print("Módulo n:", n_rsa)
print("Assinatura válida:", valida_rsa)
print(f"Tempo de ataque: {tempo_rsa:.6f} segundos")
print("Fatores:", fatores_rsa)

print("\n=== ISRSAC ===")
print("Módulo n:", n_isrsac)
print("Assinatura válida:", valida_isrsac)
print(f"Tempo de ataque: {tempo_isrsac:.6f} segundos")
print("Fatores:", fatores_isrsac)

print("\n=== ISR-RSA ===")
print("Módulo n:", n_isrrsa)
print("Assinatura válida:", valida_isrrsa)
print(f"Tempo de ataque: {tempo_isrrsa:.6f} segundos")
print("Fatores:", fatores_isrrsa)

# Comparação visual
tempos = [tempo_rsa, tempo_isrsac, tempo_isrrsa]
rotulos = ['RSA', 'ISRSAC', 'ISR-RSA']
cores = ['blue', 'green', 'red']

melhor = rotulos[tempos.index(max(tempos))]

print(f"\n✅ O esquema mais resistente à fatoração foi: {melhor}")

plt.figure(figsize=(10, 6))
plt.bar(rotulos, tempos, color=cores, width=0.5)

for i, tempo in enumerate(tempos):
    plt.text(i, tempo + max(tempos) * 0.01, f"{tempo:.6f}s", ha='center', va='bottom', fontsize=10)

plt.title("Tempo de Fatoração dos Módulos", fontsize=14)
plt.xlabel("Algoritmo", fontsize=12)
plt.ylabel("Tempo (segundos)", fontsize=12)
plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
