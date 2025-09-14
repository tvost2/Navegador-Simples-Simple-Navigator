import os, time, random
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

CAMADAS = 3

def gerar_ips_fake(qtd=50):
    return [f"10.66.0.{i+1}" for i in range(qtd)]

def criptografar_mensagem(mensagem, keys):
    dados = mensagem.encode()
    for key in reversed(keys):
        aes = AESGCM(key)
        nonce = os.urandom(12)
        dados = nonce + aes.encrypt(nonce, dados, None)
    return dados

def descriptografar_mensagem(dados, keys):
    for key in keys:
        nonce = dados[:12]
        aes = AESGCM(key)
        dados = aes.decrypt(nonce, dados[12:], None)
    return dados.decode()

def simular_roteamento(destino, camada_count=CAMADAS):
    ips = gerar_ips_fake()
    keys = [AESGCM.generate_key(128) for _ in range(camada_count)]
    circuito = list(zip(range(1, camada_count+1), ips[:camada_count], keys))
    mensagem = f"HTTP request for {destino}"
    dados = criptografar_mensagem(mensagem, keys)

    print("🔐 VPN ativada, roteando via camadas:")
    for layer, ip, _ in circuito:
        print(f"🔒 Camada {layer} → {ip}")
        time.sleep(random.uniform(0.01, 0.03))

    mensagem_final = descriptografar_mensagem(dados, keys)
    return mensagem_final