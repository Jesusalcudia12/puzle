import hashlib
import ecdsa
import random

# Cargar direcciones
with open("puzzles.txt", "r") as f:
    targets = set(line.strip() for line in f)

# Rango del Puzzle 71
MIN_RANGE = 0x400000000000000000
MAX_RANGE = 0x7fffffffffffffffff

def get_address_compressed(priv_hex):
    pk_bytes = bytes.fromhex(priv_hex.zfill(64))
    sk = ecdsa.SigningKey.from_string(pk_bytes, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    
    # Generar llave pública COMPRIMIDA (Estándar de los puzzles)
    # Si la coordenada Y es par, empieza con 02; si es impar, con 03
    public_key = vk.to_string()
    x_hex = public_key[:32]
    y_parity = public_key[63] % 2
    prefix = b'\x02' if y_parity == 0 else b'\x03'
    compressed_pubkey = prefix + x_hex
    
    # Hashes estándar
    sha256_pub = hashlib.sha256(compressed_pubkey).digest()
    ripemd160 = hashlib.new('ripemd160', sha256_pub).digest()
    vh = b'\x00' + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(vh).digest()).digest()[:4]
    
    # Base58
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    num = int.from_bytes(vh + checksum, 'big')
    res = ""
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

print(f"🚀 Escaneando en modo LOCAL (COMPRIMIDO)...")

count = 0
while True:
    random_key = random.randint(MIN_RANGE, MAX_RANGE)
    hex_key = hex(random_key)[2:]
    
    addr = get_address_compressed(hex_key)
    count += 1
    
    if addr in targets:
        print(f"\n🔥 ¡PUZZLE ENCONTRADO! Key: {hex_key}")
        with open("EXITO.txt", "a") as f:
            f.write(f"KEY: {hex_key} | ADDR: {addr}\n")
        break
        
    if count % 50000 == 0: # Actualización menos frecuente para ganar velocidad
        print(f"Llaves probadas: {count}", end="\r")
