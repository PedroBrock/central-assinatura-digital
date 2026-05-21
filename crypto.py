import hashlib
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

KEYS_DIR = Path("keys")
PRIVATE_KEY_PATH = KEYS_DIR / "private.pem"
PUBLIC_KEY_PATH  = KEYS_DIR / "public.pem"


def gerar_chaves():
    """Gera par RSA 2048 bits e salva em arquivos .pem"""
    KEYS_DIR.mkdir(exist_ok=True)

    chave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Salva chave privada
    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(chave_privada.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # Salva chave pública
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(chave_privada.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

    print("✅ Chaves RSA geradas com sucesso!")


def _carregar_chave_privada():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def _carregar_chave_publica():
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def assinar_documento(texto: str) -> bytes:
    chave_privada = _carregar_chave_privada()
    
    assinatura = chave_privada.sign(
        texto.encode("utf-8"),   
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256()          
    )
    return assinatura


def validar_assinatura(texto: str, assinatura: bytes) -> bool:
    chave_publica = _carregar_chave_publica()

    try:
        chave_publica.verify(
            assinatura,
            texto.encode("utf-8"),  
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256()        
        )
        return True
    except Exception:
        return False