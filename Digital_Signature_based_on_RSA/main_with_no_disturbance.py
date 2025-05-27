from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature

print("1. Gerando as chaves RSA...")
private_key = rsa.generate_private_key(public_exponent=65537, key_size=1024)
public_key = private_key.public_key()
print("   Chaves geradas com sucesso!\n")

# Exportar chave privada em PEM
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
print("2. Chave privada (PEM):")
print(private_pem.decode())

# Exportar chave pública em PEM
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
print("3. Chave pública (PEM):")
print(public_pem.decode())

mensagem = b"Odeio chegar cedo"
print(f"4. Mensagem a ser assinada: {mensagem.decode()}\n")

print("5. Gerando a assinatura da mensagem com a chave privada...")
assinatura = private_key.sign(
    mensagem,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
print(f"   Assinatura gerada! (bytes da assinatura: {len(assinatura)})\n")

print("6. Verificando a assinatura usando a chave pública...")
try:
    public_key.verify(
        assinatura,
        mensagem,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("   Assinatura válida! A mensagem é autêntica e não foi alterada.")
except InvalidSignature:
    print("   Assinatura inválida! A mensagem foi modificada ou a assinatura não corresponde.")

print("\nFim do processo.")
