import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def gerar_chave():
    return AESGCM.generate_key(128)